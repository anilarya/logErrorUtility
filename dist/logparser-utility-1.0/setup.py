from distutils.core import setup 
from distutils.command.install import install as _install
from subprocess import call


def _post_install(dir):
    call("bash utils/start.sh", shell = True)


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="\n************ENTER DETAILS**************\nRunning post install task")
        
setup(cmdclass={'install': install},
      name='logparser-utility', 
      version='1.0',
      description='Utility that once installed on a linux box, automatically reads nginx logs at x interval (configurable) and sends an email with 4xx and 5xx error count and URIs',
      author='Anil Arya',
      author_email='anil.kumar@hashedin.com',
      license = "GPL",
      url='https://github.com/anilarya/logErrorUtility',
      packages=[
          'utils'
      ],
      requires=['logrotate'],
     )


 
