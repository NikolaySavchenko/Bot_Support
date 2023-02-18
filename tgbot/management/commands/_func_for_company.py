from tgbot.models import Company, Tariff


def get_company(company_unp: int):
    try:
        company = Company.objects.get(unp=int(company_unp))
        return company
    except:
        return False

def create_company(company_unp: int):
    company, created = Company.objects.get_or_create(unp=int(company_unp))
    return company


def get_tariff_list():
    tariffs = Tariff.objects.all()
    return tariffs
