from models.base_model import BaseModel


class Recruiter(BaseModel):
    def __init__(self, **kwargs):
        """
            Recruiter model.
            attributes:
                pk(int): 1
                name(str): 'Example name'
                linked_id_url(str): 'wwww.linked_id_company_url.com'
                company_id(int): 1
        """
        self.pk = kwargs.get('pk')
        self.name = kwargs.get('name')
        self.linked_in_url = kwargs.get('linked_in_url')
        self.company_id = kwargs.get('company_id')
        super().__init__()


