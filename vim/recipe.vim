" Vim syntax file
" Language:	Conary Recipe
" Maintainer:	David Christian <http://www.rpath.com>
" Updated:	2006-05-15
"
syntax clear
runtime! syntax/python.vim
syn keyword conarySFunction	mainDir addAction addSource addArchive addPatch
syn keyword conarySFunction     addRedirect

syn keyword conaryGFunction     add addAll addNewGroup addReference createGroup
syn keyword conaryGFunction     addNewGroup startGroup remove removeComponents
syn keyword conaryGFunction     replace setByDefault setDefaultGroup 
syn keyword conaryGFunction     setLabelPath

syn keyword conaryBFunction 	Run Automake Configure ManualConfigure 
syn keyword conaryBFunction 	Make MakeParallelSubdir MakeInstall
syn keyword conaryBFunction 	MakePathsInstall CompilePython
syn keyword conaryBFunction 	Ldconfig Desktopfile Environment SetModes
syn keyword conaryBFunction 	Install Copy Move Symlink Link Remove Doc
syn keyword conaryBFunction 	Create MakeDirs disableParallelMake
syn keyword conaryBFunction 	ConsoleHelper Replace SGMLCatalogEntry
syn keyword conaryBFunction 	XInetdService XMLCatalogEntry TestSuite
syn keyword conaryBFunction     PythonSetup

syn keyword conaryPFunction 	NonBinariesInBindirs FilesInMandir 
syn keyword conaryPFunction 	ImproperlyShared CheckSonames CheckDestDir
syn keyword conaryPFunction 	ComponentSpec PackageSpec 
syn keyword conaryPFunction 	Config InitScript GconfSchema SharedLibrary
syn keyword conaryPFunction 	ParseManifest MakeDevices DanglingSymlinks
syn keyword conaryPFunction 	AddModes WarnWriteable IgnoredSetuid
syn keyword conaryPFunction 	Ownership ExcludeDirectories
syn keyword conaryPFunction 	BadFilenames BadInterpreterPaths ByDefault
syn keyword conaryPFunction 	ComponentProvides ComponentRequires Flavor
syn keyword conaryPFunction 	EnforceConfigLogBuildRequirements Group
syn keyword conaryPFunction 	EnforceSonameBuildRequirements InitialContents
syn keyword conaryPFunction 	FilesForDirectories LinkCount
syn keyword conaryPFunction 	MakdeDevices NonMultilibComponent ObsoletePaths
syn keyword conaryPFunction 	NonMultilibDirectories NonUTF8Filenames TagSpec
syn keyword conaryPFunction 	Provides RequireChkconfig Requires TagHandler
syn keyword conaryPFunction 	TagDescription Transient User UtilizeGroup
syn keyword conaryPFunction 	WorldWritableExecutables UtilizeUser
syn keyword conaryPFunction 	WarnWritable Strip CheckDesktopFiles

" Most destdirPolicy aren't called from recipes, except for these
syn keyword conaryPFunction     AutoDoc RemoveNonPackageFiles TestSuiteFiles
syn keyword conaryPFunction     TestSuiteLinks

syn match   conaryMacro		"%(\w*)[sd]" contained
syn match   conaryBadMacro	"%(\w*)[^sd]" contained " no final marker
syn keyword conaryArches	contained x86 x86_64
syn keyword conarySubArches	contained sse2 3dnow 3dnowext cmov i486 i586
syn keyword conarySubArches	contained i686 mmx mmxext nx sse sse2
syn keyword conaryBad		RPM_BUILD_ROOT EtcConfig InstallBucket subDir subdir 
syn cluster conaryArchFlags 	contains=conaryArches,conarySubArches
syn match   conaryArch		"Arch\.[a-z0-9.]*" contains=conaryArches,conarySubArches
syn match   conaryArch		"Arch\.[a-z0-9.]*" contains=conaryArches,conarySubArches
syn keyword conaryKeywords	name buildRequires version clearBuildReqs
syn keyword conaryUseFlag	contained pcre tcpwrappers gcj gnat selinux pam 
syn keyword conaryUseFlag	contained bootstrap python perl 
syn keyword conaryUseFlag	contained readline gdbm emacs krb builddocs 
syn keyword conaryUseFlag	contained alternatives tcl tk X gtk gnome qt
syn keyword conaryUseFlag	contained xfce gd ldap sasl pie desktop ssl kde
syn keyword conaryUseFlag	contained slang netpbm nptl ipv6 buildtests
syn keyword conaryUseFlag	contained ntpl xen dom0 domU
syn match   conaryUse		"Use\.[a-z0-9.]*" contains=conaryUseFlag

"syn match   conaryR		"r\.\w*" contains=conaryFunction

" strings
syn region pythonString		matchgroup=Normal start=+[uU]\='+ end=+'+ skip=+\\\\\|\\'+ contains=pythonEscape,conaryMacro,conaryBadMacro
syn region pythonString		matchgroup=Normal start=+[uU]\="+ end=+"+ skip=+\\\\\|\\"+ contains=pythonEscape,conaryMacro,conaryBadMacro
syn region pythonString		matchgroup=Normal start=+[uU]\="""+ end=+"""+ contains=pythonEscape,conaryMacro,conaryBadMacro
syn region pythonString		matchgroup=Normal start=+[uU]\='''+ end=+'''+ contains=pythonEscape,conaryMacro,conaryBadMacro
syn region pythonRawString	matchgroup=Normal start=+[uU]\=[rR]'+ end=+'+ skip=+\\\\\|\\'+ contains=conaryMacro,conaryBadMacro
syn region pythonRawString	matchgroup=Normal start=+[uU]\=[rR]"+ end=+"+ skip=+\\\\\|\\"+ contains=conaryMacro,conaryBadMacro
syn region pythonRawString	matchgroup=Normal start=+[uU]\=[rR]"""+ end=+"""+ contains=conaryMacro,conaryBadMacro
syn region pythonRawString	matchgroup=Normal start=+[uU]\=[rR]'''+ end=+'''+ contains=conaryMacro,conaryBadMacro


if version >= 508 || !exists("did_python_syn_inits")
  if version <= 508
   let did_python_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif


  " The default methods for highlighting.  Can be overridden later
  "HiLink pythonStatement	Statement
  "HiLink pythonFunction	Function
  "HiLink pythonConditional	Conditional
  "HiLink pythonRepeat		Repeat
  "HiLink pythonString		String
  "HiLink pythonRawString	String
  "HiLink pythonEscape		Special
  "HiLink pythonOperator		Operator
  "HiLink pythonPreCondit	PreCondit
  "HiLink pythonComment		Comment
  "HiLink pythonTodo		Todo
  HiLink conaryMacro		Special
  HiLink conaryBFunction	Function
  HiLink conaryGFunction        Function
  HiLink conarySFunction	Operator
  HiLink conaryPFunction	Typedef
  HiLink conaryFlags		PreCondit
  HiLink conaryArches		Special
  HiLink conarySubArches	Special
  HiLink conaryBad		Error
  HiLink conaryBadMacro		Error
  HiLink conaryKeywords		Special
  HiLink conaryUseFlag		Typedef
  "HiLink conaryR		Typedef

  delcommand HiLink
endif

let b:current_syntax = "recipe"

" vim: ts=8
