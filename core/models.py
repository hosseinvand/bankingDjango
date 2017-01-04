from django.contrib.auth.models import User  # multiple models have keys
# Employee subclass and maintainer
# to user so collusions!
from django.db import models
from django.core.exceptions import ValidationError
import uuid


UNKNOWN = 'NA'
ACCEPT = 'AC'
REJECT = 'RE'
statuses = (
    (UNKNOWN, 'unknown'),
    (ACCEPT, 'accepted'),
    (REJECT, 'rejected'),
)

DAY = "da"
WEEK = "we"
MONTH = "mo"
YEAR = "yr"
period_types = (
    (DAY, "daily"),
    (WEEK, "weekly"),
    (MONTH, "monthly"),
    (YEAR, "yearly"),
)

NONE = "NON"
SMS = "SMS"
MAIL = "MAL"
BOTH = "BOT"
notif_types = (
    (NONE, "none"),
    (SMS, "sms"),
    (MAIL, "E-Mail"),
    (BOTH, "both"),
)

REAL = 'R'
LEGAL = 'L'
customer_types = (
    (REAL, "real"),
    (LEGAL, "legal"),
)

WITHDRAW = 'w'
DEPOSIT = 'd'
transaction_types = (
    (WITHDRAW, 'withdraw'),
    (DEPOSIT, 'deposit'),
)

CARD_TO_CARD = "CTC"
TRANSACTION = "TRN"
wage_types = (
    (CARD_TO_CARD, "card to card"),
    (TRANSACTION, "transaction"),
)


class System(models.Model):
    card_production_fee = models.IntegerField(default=100)
    cheque_production_fee = models.IntegerField(default=100)
    sms_notif_fee = models.IntegerField(default=100)
    card_to_card_fee = models.IntegerField(default=100)
    transactio_fee = models.IntegerField(default=100)
    atm_min_money = models.IntegerField(default=100000)
    loan_interest = models.FloatField(default=0.14)
    deposit_yearly_interest = models.FloatField(default=0.10)
    # Implemented yearly, but must be applied daily(x^(1/365)).

    def __str__(self):
        return "System Settings"


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    father_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    email = models.CharField(max_length=255)

    notif_type = models.CharField(
        max_length=3,
        default=NONE,
        choices=notif_types,
    )

    def __str__(self):
        return str(self.pk)
        + " "
        + self.first_name
        + " "
        + self.last_name


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="notifications",
    )

    text = models.TextField(max_length=1023)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return "{}, Seen:{}".format(
            self.user.username,
            self.seen,
        )


class Maintainer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        related_name='+',
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name
        + " "
        + self.last_name


class Greenback(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)


class ATM(models.Model):
    balance = models.IntegerField()
    maintainer = models.ForeignKey(
        Maintainer,
        on_delete=models.SET_NULL,
        related_name="atms",
        null=True,
    )

    greenback = models.ManyToManyField(
        Greenback,
        through='Contain',
        related_name='+',
    )

    def __str__(self):
        return "atm:{} - balance:{}".format(
            self.pk,
            self.balance,
        )


class Contain(models.Model):
    greenback = models.ForeignKey(
        Greenback,
        on_delete=models.PROTECT,
        related_name='+',
    )

    atm = models.ForeignKey(
        ATM,
        on_delete=models.PROTECT,
        related_name='+',
    )

    count = models.IntegerField(default=0)


class Account(models.Model):
    real_owner = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        null=True,
        related_name="accounts",
    )

    account_number = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)

    user_type = models.CharField(
        max_length=1,
        choices=customer_types,
        default=REAL,
    )

    def __str__(self):
        return str(self.account_number)


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        unique=True,
        null=True,
        related_name='+',
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    social_id = models.CharField(
        max_length=10,
        unique=True,
    )

    branch = models.ForeignKey(
        'Branch',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )

    class Meta:
        abstract = True


class Manager(Employee):

    def __str__(self):
        return self.first_name
        + " "
        + self.last_name


class Auditor(Employee):

    def __str__(self):
        return self.first_name
        + " "
        + self.last_name


class Cashier(Employee):

    def __str__(self):
        return self.first_name
        + " "
        + self.last_name


class Jursit(Employee):

    def __str__(self):
        return self.first_name
        + " "
        + self.last_name


class Branch(models.Model):
    manager = models.ForeignKey(
        Manager,
        on_delete=models.PROTECT,
        null=True,
        related_name='+',
    )

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    amount = models.IntegerField()
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        related_name="transactions",
        null=True,
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
    )

    auditor = models.ForeignKey(
        Auditor,
        on_delete=models.PROTECT,
        related_name='transactions',
    )

    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    transaction_type = models.CharField(
        max_length=1,
        choices=transaction_types,
    )

    def __str__(self):
        return "{} {}  account: {} @ {} {} ".format(
            self.amount,
            self.transaction_type,
            self.account.pk,
            self.date,
            self.time,
        )


class TransactionWage(models.Model):
    amount = models.IntegerField()
    wage_type = models.CharField(
        max_length=3,
        choices=wage_types,
    )

    amount = models.IntegerField()
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.PROTECT,
        related_name="wage",
    )  # Points to the transaction that are of type w.
    # So related_name=wage_type only must be used
    # when the type of transaction is w.


class Card(models.Model):
    card_number = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    account = models.OneToOneField(
        Account,
        on_delete=models.PROTECT,
        related_name="card",
    )

    def __str__(self):
        return str(self.card_number)


class WithdrawFromATM(models.Model):
    ATM = models.ForeignKey(
        ATM,
        on_delete=models.SET_NULL,
        related_name="withdrawals",
        null=True,
    )

    card = models.ForeignKey(
        Card,
        on_delete=models.PROTECT,
        related_name="withdrawals",
        null=True,
    )

    amount = models.IntegerField()

    def __str__(self):
        return "withdraw form {} @ {} for {} $".format(
            self.card.card_number,
            self.ATM.pk,
            self.amount,
        )


class CardToCard(models.Model):
    amount = models.IntegerField()

    from_card = models.ForeignKey(
        Card,
        on_delete=models.PROTECT,
        related_name="from_cards",
    )

    to_card = models.ForeignKey(
        Card,
        on_delete=models.PROTECT,
        related_name="to_cards",
    )

    deposit = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name='+',
    )

    withdraw = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name='+',
    )

    atm = models.ForeignKey(
        ATM,
        on_delete=models.SET_NULL,
        related_name="card_to_cards",
        null=True,
    )

    def __str__(self):
        return "{} from {} to {}".format(
            self.amount,
            self.from_card,
            self.to_card,
        )


class BillType(models.Model):
    company = models.CharField(max_length=255)
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="legal_owners",
    )

    def __str__(self):
        return self.company


class Bill(models.Model):
    bill_type = models.ForeignKey(
        BillType,
        on_delete=models.PROTECT,
        related_name="bills",
    )

    amount = models.IntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return "Bill: {} amount: {} is paid: {}".format(
            self.bill_type.company,
            self.amount,
            self.paid,
        )


class PayedBill(models.Model):
    payment = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name='+',
    )  # Keep in mind that this always points to deposit transaction

    bill = models.OneToOneField(
        Bill,
        on_delete=models.PROTECT,
        related_name="payment_info",
    )

    def __str__(self):
        return self.bill.bill_type.company


class LoanApplication(models.Model):
    amount = models.IntegerField()
    payment_count = models.IntegerField()
    legal_expert_validation = models.CharField(
        max_length=2,
        choices=statuses,
        default=UNKNOWN,
    )

    auditor_validation = models.CharField(
        max_length=2,
        choices=statuses,
        default=UNKNOWN,
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="loan_applications",
    )

    def __str__(self):
        return "Balance: {} Owner: {}".format(
            self.amount,
            self.account.pk,
        )


class Loan(models.Model):
    remaining_payments = models.IntegerField()
    interest = models.FloatField()
    loan_application = models.OneToOneField(
        LoanApplication,
        on_delete=models.PROTECT,
        related_name="loan",
    )

    def __str__(self):
        return "Balance: {} Owner: {}".format(
            self.loan_application.balance,
            self.loan_application.account.pk,
        )

    def clean(self):
        if (self.loan_application.legal_expert_validation is not ACCEPT or
                self.loan_application.auditor_validation is not ACCEPT):
            raise ValidationError(
                "Can't make loan for lack of validation"
            )


class Inquiry(models.Model):
    status = models.CharField(
        max_length=2,
        choices=statuses,
        default=UNKNOWN,
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
    )

    def __str__(self):
        return "Account: {} stat: {}".format(
            self.account.account_number,
            self.status,
        )


class ChequeApplication(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="cheque_books",
    )

    legal_expert_validation = models.CharField(
        max_length=2,
        choices=statuses,
        default=UNKNOWN,
    )
    auditor_validation = models.CharField(
        max_length=2,
        choices=statuses,
        default=UNKNOWN,
    )
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "cheque book belonging to " + str(self.account.pk)


class Cheque(models.Model):
    cheque_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    cheque_application = models.ForeignKey(
        ChequeApplication,
        related_name="cheque_pages",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return str(self.cheque_id)

    def clean(self):
        if (self.cheque_application.legal_expert_validation != ACCEPT):
            raise ValidationError(
                "Can't make cheque page for lack of legal validation it is {}".format(
                    self.cheque_application.legal_expert_validation,
                )
            )
            print(self.cheque_application.legal_expert_validation)

        if(self.cheque_application.auditor_validation != ACCEPT):
            raise ValidationError(
                "Can't make cheque page for lack of auditor validation{}".format(
                    self.cheque_application.legal_expert_validation,
                )
            )


class ChequeIssue(models.Model):
    date = models.DateField()
    cheque = models.OneToOneField(
        Cheque,
        on_delete=models.PROTECT,
        related_name="issue",
    )

    amount = models.IntegerField()
    legal_expert_validation = models.BooleanField(default=False)
    auditor_validation = models.BooleanField(default=False)
    dest = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
    )  # keep in mind that this always points to withdraw transaction


class PaymentOrder(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="payment_orders_from",
    )

    dest = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='payment_orders_to',
    )

    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "Havale from {} Amount: {} TimeSpan: {} - {}".format(
            self.account.pk,
            self.amount,
            self.start_date,
            self.end_date
        )
