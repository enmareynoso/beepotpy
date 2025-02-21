from faker import Faker
import random

class FakeEnterprise:
    def __init__(self):
        self.fake = Faker()
        self.company = self._generate_company()
        self.users = self._generate_users()
        self.network = self._generate_network()
        
    def _generate_company(self):
        return {
            'name': self.fake.company(),
            'domain': self.fake.domain_name(),
            'industry': self.fake.bs(),
            'foundation_date': self.fake.date_between('-30y', '-1y')
        }
    
    def _generate_users(self):
        return [{
            'username': self.fake.user_name(),
            'password': self.fake.password(length=12),
            'email': self.fake.company_email(),
            'role': random.choice(['admin', 'dev', 'sysadmin']),
            'last_login': self.fake.date_time_this_year()
        } for _ in range(random.randint(8, 15))]

    def _generate_network(self):
        return {
            'subnet': self.fake.ipv4_private(),
            'gateway': self.fake.ipv4_private(),
            'dns': [self.fake.ipv4_private() for _ in range(2)],
            'public_ip': self.fake.ipv4_public()
        }