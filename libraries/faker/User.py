class generate_user:
    def __init__(self, first_name, last_name, job, address, phone_number, city, state, zip_code, domain_name, prefix, suffix):
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.address = address
        self.phone_number = phone_number
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.domain_name= domain_name
        self.prefix = prefix
        self.suffix = suffix
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    @property
    def email(self):
        return f'{self.first_name}.{self.last_name}@{self.domain_name}'
