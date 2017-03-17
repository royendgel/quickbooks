# Automatically generated from script.

from recources_super_classes import CreateMixin, DeleteMixin, Resource, RetriveMixin, UpdateMixin


class Entity(RetriveMixin):
    methods = ["query"]
    version_query = 1


class ItemReceipt(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 3
    version_add = 4
    version_mod = 4


class AccountTaxLineInfo(RetriveMixin):
    methods = ["query"]
    version_query = 7


class Vehicle(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 6
    version_add = 6
    version_mod = 6


class DateDrivenTerms(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class Transfer(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 12
    version_add = 12
    version_mod = 12


class TxnDeleted(RetriveMixin):
    methods = ["query"]
    version_query = 2


class CreditCardCredit(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 6


class CreditCardCharge(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 6


class BarCode(RetriveMixin):
    methods = ["query"]
    version_query = 12


class ReceivePaymentToDeposit(RetriveMixin):
    methods = ["query"]
    version_query = 2


class SalesReceipt(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 5


class DataExt(CreateMixin, UpdateMixin):
    methods = ["add", "mod"]
    version_add = 2
    version_mod = 2


class StandardTerms(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class TimeTracking(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 6


class GeneralSummaryReport(RetriveMixin):
    methods = ["query"]
    version_query = 2


class Customer(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 1


class SalesTaxReturn(RetriveMixin):
    methods = ["query"]
    version_query = 0


class ItemOtherCharge(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class JournalEntry(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 6


class Account(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 6


class ItemService(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 1


class SalesRep(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class ItemDiscount(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class ItemSites(RetriveMixin):
    methods = ["query"]
    version_query = 10


class Preferences(RetriveMixin):
    methods = ["query"]
    version_query = 1.1


class Item(RetriveMixin):
    methods = ["query"]
    version_query = 1


class Charge(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2
    version_add = 2
    version_mod = 3


class ItemSalesTaxGroup(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class DataEventRecoveryInfo(RetriveMixin):
    methods = ["query"]
    version_query = 3


class BillToPay(RetriveMixin):
    methods = ["query"]
    version_query = 2


class Estimate(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class SalesTaxPaymentCheck(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2
    version_add = 9
    version_mod = 9


class PayrollItemNonWage(RetriveMixin):
    methods = ["query"]
    version_query = 3


class ToDo(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 9


class Check(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 6


class JobType(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class ItemInventory(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 1


class PurchaseOrder(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 2.1


class VendorType(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class Host(RetriveMixin):
    methods = ["query"]
    version_query = 1


class Vendor(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 1


class TransferInventory(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 10
    version_add = 10
    version_mod = 10


class UnitOfMeasureSet(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 7
    version_add = 7


class VehicleMileage(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 6
    version_add = 6


class ListDeleted(RetriveMixin):
    methods = ["query"]
    version_query = 2


class ShipMethod(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class PayrollLastPeriod(RetriveMixin):
    methods = ["query"]
    version_query = 0


class BudgetSummaryReport(RetriveMixin):
    methods = ["query"]
    version_query = 3


class ItemNonInventory(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 1


class SpecialAccount(CreateMixin):
    methods = ["add"]
    version_add = 6


class SpecialItem(CreateMixin):
    methods = ["add"]
    version_add = 6


class Company(RetriveMixin):
    methods = ["query"]
    version_query = 1


class PayrollItemWage(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 2


class CreditMemo(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class PriceLevel(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 4
    version_add = 4
    version_mod = 4


class BillPaymentCreditCard(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 2
    version_add = 2


class BillingRate(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 6
    version_add = 6


class InventoryAdjustment(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2
    version_add = 2
    version_mod = 9


class Class(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 8


class CustomerMsg(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class Deposit(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2
    version_add = 2
    version_mod = 7


class ItemAssembliesCanBuild(RetriveMixin):
    methods = ["query"]
    version_query = 5


class Terms(RetriveMixin):
    methods = ["query"]
    version_query = 1


class OtherName(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 1


class ARRefundCreditCard(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 5
    version_add = 5


class JobReport(RetriveMixin):
    methods = ["query"]
    version_query = 2


class ItemFixedAsset(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 3
    version_add = 3
    version_mod = 3


class ItemSubtotal(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class Employee(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 1


class GeneralDetailReport(RetriveMixin):
    methods = ["query"]
    version_query = 2


class PayrollSummaryReport(RetriveMixin):
    methods = ["query"]
    version_query = 3


class Invoice(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 2.1


class AgingReport(RetriveMixin):
    methods = ["query"]
    version_query = 2


class SalesOrder(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2.1
    version_add = 2.1
    version_mod = 3


class CustomDetailReport(RetriveMixin):
    methods = ["query"]
    version_query = 2


class PayrollDetailReport(RetriveMixin):
    methods = ["query"]
    version_query = 3


class DataExtDef(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2
    version_add = 2
    version_mod = 2


class VendorCredit(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 8


class TimeReport(RetriveMixin):
    methods = ["query"]
    version_query = 2


class BuildAssembly(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 5
    version_add = 5
    version_mod = 5


class CustomerType(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class ItemGroup(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class Template(RetriveMixin):
    methods = ["query"]
    version_query = 3


class ItemSalesTax(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class CompanyActivity(RetriveMixin):
    methods = ["query"]
    version_query = 2


class ListDisplay(CreateMixin, UpdateMixin):
    methods = ["add", "mod"]
    version_add = 3
    version_mod = 3


class WorkersCompCode(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 7
    version_add = 7
    version_mod = 7


class ReceivePayment(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1.1
    version_add = 1.1
    version_mod = 6


class Bill(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class ItemInventoryAssembly(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2
    version_add = 2
    version_mod = 3


class Currency(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 8
    version_add = 8
    version_mod = 8


class ItemPayment(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 3


class SalesTaxReturnLine(RetriveMixin):
    methods = ["query"]
    version_query = 0


class Form1099CategoryAccountMapping(UpdateMixin, RetriveMixin):
    methods = ["mod", "query"]
    version_query = 8
    version_mod = 8


class BillPaymentCheck(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 2
    version_add = 2
    version_mod = 6


class TxnDisplay(CreateMixin, UpdateMixin):
    methods = ["add", "mod"]
    version_add = 3
    version_mod = 3


class PaymentMethod(CreateMixin, RetriveMixin):
    methods = ["add", "query"]
    version_query = 1
    version_add = 1


class ClearedStatus(UpdateMixin):
    methods = ["mod"]
    version_mod = 2


class InventorySite(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 10
    version_add = 10
    version_mod = 10


class Transaction(RetriveMixin):
    methods = ["query"]
    version_query = 4


class CustomSummaryReport(RetriveMixin):
    methods = ["query"]
    version_query = 2


class SalesTaxCode(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 1
    version_add = 1
    version_mod = 8


class Lead(CreateMixin, UpdateMixin, RetriveMixin):
    methods = ["add", "mod", "query"]
    version_query = 13
    version_add = 13
    version_mod = 13


class SalesTaxPayable(RetriveMixin):
    methods = ["query"]
    version_query = 9


