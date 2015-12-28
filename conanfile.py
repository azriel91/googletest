from conans import *
import subprocess

class GoogleTestConan(ConanFile):
    name = 'googletest'
    version = '1.7.0'
    settings = ['os', 'compiler', 'build_type']
    generators = ['cmake']
    exports = subprocess.check_output(['git', 'ls-files']).split()
    options = {
        'BUILD_SHARED_LIBS':      ['ON', 'OFF'], # Build shared libraries (DLLs).
        'gtest_force_shared_crt': ['ON', 'OFF'], # Use shared (DLL) run-time lib even when Google Test is built as static lib.
        'gtest_build_tests':      ['ON', 'OFF'], # Build all of gtest's own tests.
        'gtest_build_samples':    ['ON', 'OFF'], # Build gtest's sample programs.
        'gtest_disable_pthreads': ['ON', 'OFF'], # Disable uses of pthreads in gtest.

        # Set this to 0 if your project already uses a tuple library, and GTest should use that library
        # Set this to 1 if GTest should use its own tuple library
        'GTEST_USE_OWN_TR1_TUPLE': [None, '0', '1'],

        # Set this to 0 if GTest should not use tuple at all. All tuple features will be disabled
        'GTEST_HAS_TR1_TUPLE': [None, '0'],

        # If GTest incorrectly detects whether or not the pthread library exists on your system, you can force it
        # by setting this option value to:
        #   1 - if pthread does actually exist
        #   0 - if pthread does not actually exist
        'GTEST_HAS_PTHREAD': [None, '0', '1']
    }
    default_options = (
                        'BUILD_SHARED_LIBS=OFF',
                        'gtest_force_shared_crt=OFF',
                        'gtest_build_tests=OFF',
                        'gtest_build_samples=OFF',
                        'gtest_disable_pthreads=OFF',
                        'GTEST_USE_OWN_TR1_TUPLE=None',
                        'GTEST_HAS_TR1_TUPLE=None',
                        'GTEST_HAS_PTHREAD=None'
                      )

    build_dir = 'build'

    def build(self):
        option_defines = ' '.join("-D%s=%s" % (opt, val) for (opt, val) in self.options.iteritems() if val is not None)
        self.run("cmake . -B{build_dir} {defines}".format(build_dir=self.build_dir, defines=option_defines))
        self.run("cmake --build {build_dir}".format(build_dir=self.build_dir))

    def package(self):
        self.copy('*', dst='cmake', src='cmake')
        self.copy('*', dst='include', src='include')
        self.copy('CMakeLists.txt', dst='.', src='.')

        # Meta files
        self.copy('CHANGES', dst='.', src='.')
        self.copy('CONTRIBUTORS', dst='.', src='.')
        self.copy('LICENSE', dst='.', src='.')
        self.copy('README', dst='.', src='.')

        # Built artifacts
        if self.options['BUILD_SHARED_LIBS'] == 'ON':
            self.copy('libgtest.so', dst='lib', src=self.build_dir)
            self.copy('libgtest_main.so', dst='lib', src=self.build_dir)
        else:
            self.copy('libgtest.a', dst='lib', src=self.build_dir)
            self.copy('libgtest_main.a', dst='lib', src=self.build_dir)

        # IDE sample files (commented code intentionally left here)
        # self.copy('*', dst='codegear', src='codegear')
        # self.copy('*', dst='m4', src='m4')
        # self.copy('*', dst='make', src='make')
        # self.copy('*', dst='msvc', src='msvc')
        # self.copy('*', dst='xcode', src='xcode')

        # Autoconf/Automake
        # self.copy('configure.ac', dst='configure.ac', src='.')
        # self.copy('Makefile.am', dst='Makefile.am', src='.')

        # self.copy('*', dst='samples', src='samples')

        # Files not used by downstream
        # self.copy('*', dst='build-aux', src='build-aux')
        # self.copy('*', dst='scripts', src='scripts')
        # self.copy('*', dst='test', src='test')

        # google mock compiles with gtest sources
        self.copy('*', dst='src', src='src')
