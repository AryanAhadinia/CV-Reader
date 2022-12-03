from PyPDF2 import PdfReader
from hazm import Normalizer

from cv_info_extractor.city_extractor import CityProvinceExtractor
from cv_info_extractor.email_detector import EmailDetection
from cv_info_extractor.emp_stat_extractor import EmploymentStatusExtractor
from cv_info_extractor.expected_salary_extractor import ExpectedSalaryExtractor
from cv_info_extractor.job_expected_extractor import JobExpectedExtractor
from cv_info_extractor.name_detector import NameDetection
from cv_info_extractor.phone_number_detector import PhoneNumberDetection
from cv_info_extractor.date_extractor import DateDetection
from cv_info_extractor.section_extractor import SectionExtractor
from utils import CusNormalizer
from utils.job_experience_section_extractor import JobExpSecExtraction


def run(address):
    final_text = ''
    result = {}
    reader = PdfReader(address)
    for page in reader.pages:
        text = page.extract_text()
        final_text += text
    email = EmailDetection().find_email(final_text)
    normalizer = Normalizer()
    final_text = normalizer.normalize(final_text)
    final_text = CusNormalizer().normalize(final_text)
    # print(final_text)
    result['ایمیل'] = email
    full_name, first_name, last_name = NameDetection().find_name(final_text)
    result['نام'] = first_name
    result['نام خانوادگی'] = last_name
    phone_number = PhoneNumberDetection().find_phone_number(final_text)
    result['شماره تماس'] = phone_number
    date = DateDetection().find_date_number(final_text)
    result['تاریخ تولد'] = date
    city = CityProvinceExtractor().find(final_text)[0]
    result['استان محل سکونت'] = city['province']
    result['شهر محل سکونت'] = city['city']
    extra, first_sec = SectionExtractor().find_sections(final_text)
    for info in extra:
        if type(info) == dict:
            result.update(info)
    job_section = JobExpSecExtraction().extract(result)
    result['وضعیت اشتغال'] = EmploymentStatusExtractor().find(final_text, job_section)
    result['نوع شغل موردنظر'] = JobExpectedExtractor().find(final_text)
    result['حقوق موردانتظار'] = ExpectedSalaryExtractor().find(final_text)
    print(result)
    return result
