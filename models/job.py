from models.base_model import BaseModel


class Job(BaseModel):
    def __init__(self, **kwargs):
        """
            Job model.
            attributes:
                pk(int): 1
                title(str): 'Example job'
                description(str): 'Example job description'
                type(str): 'Mid-level'
                location(str): 'Colombia'
                already_applied(bool): False -> default
                posted_date(Datetime): Datetime object
                recruiter_id(int): 1
                company_id(int): 1
        """
        self.pk = kwargs.get('pk')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.type = kwargs.get('type')
        self.location = kwargs.get('location', 'Anywhere')
        self.already_applied = kwargs.get('already_applied', False)
        self.posted_date = kwargs.get('posted_date')
        self.recruiter_id = kwargs.get('recruiter_id')
        self.company_id = kwargs.get('company_id')
        super().__init__()
