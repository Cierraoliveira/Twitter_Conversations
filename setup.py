from distutils.core import setup
setup(
  name = 'Twitter_Conversations',         # How you named your package folder (MyLib)
  packages = ['Twitter_Conversations'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This scrapes twitter conversations',   # Give a short description about your library
  author = 'Cierra Oliveira',                   # Type in your name
  author_email = 'cierraoliveira@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/Cierraoliveira',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Cierraoliveira/Twitter_Conversations/archive/v_02.tar.gz', 
  keywords = ['Twitter', 'Tweepy', 'Twint'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Tweepy',
          'Twint',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',  
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
