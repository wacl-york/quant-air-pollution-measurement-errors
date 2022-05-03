from setuptools import setup, find_packages

setup(name='quantpy',
      version='0.1.0',
      description='Provides tools for evaluating errors in low cost sensor air quality measurements',
      url='https://github.com/wacl-york/quant-measurement-errors-tools/quantpy',
      author='Sebastian Diez',
      author_email='sebastian_diez@hotmail.com',
      license='MIT',
      install_requires=[
          "pandas",
          "matplotlib",
          "numpy",
          "scipy",
          "sklearn"
      ],
      packages=find_packages(include=["quantpy", "quantpy.*"]),
      zip_safe=False
)
