from distutils.core import setup


with open("README.rst", "r", encoding="utf-8") as f:
    README = f.read()

setup(
  name = 'easy_api_builder',         
  packages = ['easy_api_builder', "easy_api_builder.templates"], 
  version = '0.3.1',     
  license='MIT',     
  long_description=README,
  long_description_content_type='text/x-rst',
  include_package_data=True,   
  description = 'The easy way to create powerful apis in python', 
  install_requires = ["Flask", "requests"],
  author = 'Areo',        
  url = 'https://github.com/areoxy/easy_api_builder',  
  download_url = 'https://github.com/Areoxy/easy_api_builder/releases/tag/easy_api_builder_v0.3.1',    
  keywords = ['api', 'easy', 'api_maker', "requests", "api_builder"],   
  project_urls={
        "Documentation": "https://github.com/areoxy/easy_api_builder",
        "Issue tracker": "https://github.com/areoxy/easy_api_builder/issues",
      },
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
    'Programming Language :: Python :: 3.10',
  ]
)
