from conans import ConanFile, CMake

class GlfwExamplesConan(ConanFile):
   settings = "os", "compiler", "build_type", "arch"
   requires = "glfw/3.2.1@bincrafters/stable"
   generators = "cmake"
   default_options = "glfw:shared=False"

   def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

   def imports(self):
      self.copy("*.dll", dst="bin", src="bin")
      self.copy("*.dylib*", dst="bin", src="lib")