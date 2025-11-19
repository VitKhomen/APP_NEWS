# backend/apps/subscribe/management/commands/fix_stripe_integration.py
import stripe
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.subscribe.models import SubscriptionPlan

stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = 'Fix Stripe integration by creating real products and prices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreate even if stripe_price_id exists',
        )

    def handle(self, *args, **options):
        force = options['force']

        # перевіряєм підключення до Stripe
        try:
            stripe.Balance.retrieve()
            self.stdout.write(self.style.SUCCESS(
                '✅ Підключення до Stripe працює'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'❌ Помилка підключення до Stripe: {e}'))
            return

        # Обробляємо усі плани
        plans = SubscriptionPlan.objects.filter(is_active=True)

        for plan in plans:
            self.stdout.write(f'Обробляємо план: {plan.name}')

            # Перевіряємо чи потрібно створити
            if plan.stripe_price_id and not force and plan.stripe_price_id.startswith('price_1'):
                self.stdout.write(
                    f'  ⏭️ План вже має реальний Stripe ID: {plan.stripe_price_id}')
                continue

            try:
                # Створюємо чи обробляємо продукт
                product = stripe.Product.create(
                    name=plan.name,
                    description=f"Subscription plan: {plan.name}",
                    metadata={
                        'plan_id': plan.id,
                        'django_model': 'SubscriptionPlan',
                        'created_by': 'django_management_command'
                    }
                )
                self.stdout.write(f'  ✅ Продукт створено: {product.id}')

                # Створюємо цену
                price = stripe.Price.create(
                    product=product.id,
                    unit_amount=int(plan.price * 100),  # В центах
                    currency='usd',
                    recurring={'interval': 'month'},
                    metadata={
                        'plan_id': plan.id,
                        'django_model': 'SubscriptionPlan'
                    }
                )
                self.stdout.write(f'  ✅ Цена створена: {price.id}')

                # Оновлюємо план
                old_id = plan.stripe_price_id
                plan.stripe_price_id = price.id
                plan.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✅ План оновлен: {old_id} → {price.id}'
                    )
                )

            except stripe.error.StripeError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'  ❌ Помилка Stripe для плана {plan.name}: {e}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'  ❌ Обща помилка для плана {plan.name}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                '🎉 Обробка закінчена! Перевіряйте Stripe Dashboard.')
        )
