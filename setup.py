from distutils.core import setup


with open("README.rst", "r", encoding="utf-8") as f:
    README = f.read()

setup(
  name = 'easy_api_builder',         
  packages = ['easy_api_builder'], 
  version = '0.1',     
  license='MIT',     
  package_data={
        'easy_api_builder': ['templates/*']
  },
  long_description=README,
  long_description_content_type='text/x-rst',
  include_package_data=True,   
  description = 'easy_api_builder is an easy way to create you own API in python', 
  install_requires = "Flask",
  author = 'Areo',  
  author_email = 'areo@envyre.de',      
  url = 'https://github.com/Envyre-Development/easy_api_builder',  
  download_url = 'https://github.com/Envyre-Development/easy_api_builder/archive/refs/tags/easy_api_builder.tar.gz',    
  keywords = ['api', 'easy', 'api_maker'],   
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ]
)