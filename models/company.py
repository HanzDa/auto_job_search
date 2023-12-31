from models.base_model import BaseModel


class Company(BaseModel):
    def __init__(self, **kwargs):
        """
            Company model.
            attributes:
                pk(int): 1
                name(str) required: 'Example name'
                linked_id_url(str): 'wwww.linked_id_company_url.com'
                industry(str): 'Tech'
        """
        self.pk = kwargs.get('pk')
        self.name = kwargs.get('name')
        self.linked_in_url = kwargs.get('linked_in_url')
        self.industry = kwargs.get('industry')
        super().__init__()

    class Meta:
        table_name = 'companies'
