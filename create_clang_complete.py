 @register_command("clang")
 class ClangProject(NodeCommand):
     def __init__(self):
         super(ClangProject, self).__init__()
         self.content = []
 
     usage = "Usage: condor.py clang <cmd> [options]"
     def help(self):
         return """Create .clang_complete file for a node and its dependencies"""
 
     def node_exec(self, path, graph):
         # save root node for filename
         # Work only on dependencies with code
         dep = buildDep(path, wc_base_path=self.dg.wc_base_path)
         if not (dep.getLevel() == "module" and dep.getCodeType() == "application"):
             return False
         self.content.append(path)
         print("Processing [%s]" % path)
         return True
 
     def process_output(self, result, output, notifications):
         self.content.sort(key=lambda s: s[0].lower())
         f = open('.clang_complete', 'w')
         f.write('-std=gnu++98\r\n')
         f.write('-Iinclude\r\n')
         [ f.write('-I' +x[0] + '\r\n') for x in os.walk('src')]
         f.write('-I/usr/include\r\n')
         f.write('-I/usr/local/include\r\n')
         for item in self.content:
             f.write('-I' + item + '/include\r\n')
         f.close()
         return super(ClangProject, self).process_output(result, output, notifications)
