import os

def get_info():
    print("Choisis la version du mod :")
    print("1. 1.12.2")
    print("2. 1.20.6 (Soon)")

    version = input("Choix : ")
    if version != "1":
        print("Seule la version 1.12.2 est disponible pour le moment")
        return None

    mod_name = input("Nom du mod (ex: SunsetRP) : ")
    modid = input("Mod ID (ex: sunset) : ")
    author = input("Auteur du mod (ex: Alouchi) : ")
    package_prefix = input("Package prefix (ex: fr / com / net) : ")
    description = input("Description de votre mod : ")
    main_class = input("Nom de la classe principale (ex: Main) : ")

    print("Mod généré avec succès")

    return {
        "version": "1.12.2",
        "mod_name": mod_name,
        "modid": modid,
        "package": package_prefix + "." + modid,
        "description": description,
        "author": author,
        "main_class": main_class
    }


def create_mod_base(info):
    base_path = info["mod_name"]
    package_path = os.path.join(base_path, "src", "main", "java", *info["package"].split('.'))
    mainmod_path = os.path.join(base_path, "src", "main", "java", *info["package"].split('.'), "main")
    resource_path = os.path.join(base_path, "src", "main", "resources")
    
    os.makedirs(package_path, exist_ok=True)
    os.makedirs(resource_path, exist_ok=True)
    os.makedirs(mainmod_path, exist_ok=True)

    # PROXY
    clientmodprox_path = os.path.join(base_path, "src", "main", "java", *info["package"].split('.'), "main", "proxy", "client")
    commonmodprox_path = os.path.join(base_path, "src", "main", "java", *info["package"].split('.'), "main", "proxy", "common")
    servermodprox_path = os.path.join(base_path, "src", "main", "java", *info["package"].split('.'), "main", "proxy", "server")

    os.makedirs(clientmodprox_path, exist_ok=True)
    os.makedirs(commonmodprox_path, exist_ok=True)
    os.makedirs(servermodprox_path, exist_ok=True)

    # CLASSES

    main_path = os.path.join(mainmod_path, "Main.java")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(generate_main_class(info))

    reference_path = os.path.join(mainmod_path, "Reference.java")
    with open(reference_path, "w", encoding="utf-8") as f:
        f.write(generate_reference_class(info))

    module_path = os.path.join(package_path, "IModule.java")
    with open(module_path, "w", encoding="utf-8") as f:
        f.write(generate_module_class(info))

    clientprox_path = os.path.join(clientmodprox_path, "ClientProxy.java")
    with open(clientprox_path, "w", encoding="utf-8") as f:
        f.write(generate_client_proxy_class(info))

    commonprox_path = os.path.join(commonmodprox_path, "CommonProxy.java")
    with open(commonprox_path, "w", encoding="utf-8") as f:
        f.write(generate_common_proxy_class(info))

    serverprox_path = os.path.join(servermodprox_path, "ServerProxy.java")
    with open(serverprox_path, "w", encoding="utf-8") as f:
        f.write(generate_server_proxy_class(info))


    # RACINE

    gradle_path = os.path.join(base_path, "build.gradle")
    with open(gradle_path, "w", encoding="utf-8") as f:
        f.write(generate_bgradle_class(info))

    gradlew_bat_path = os.path.join(base_path, "gradlew.bat")
    with open(gradlew_bat_path, "w", encoding="utf-8") as f:
        f.write(generate_gradlew_bat(info))
    
    gradlew_path = os.path.join(base_path, "gradlew")
    with open(gradlew_path, "w", encoding="utf-8") as f:
        f.write(generate_gradlew_class(info))

    gitignore_path = os.path.join(base_path, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(generate_gitignore_class(info))

    # RESOURCES

    mcmodinfo_path = os.path.join(resource_path, "mcmod.info")
    with open(mcmodinfo_path, "w", encoding="utf-8") as f:
        f.write(generate_mcmod_class(info))    

    gitignore_path = os.path.join(resource_path, "pack.mcmeta")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(generate_mcmeta_class(info))    

def generate_main_class(info):
    base_package = info['package']  # ex: fr.alouchi.monmod

    return f"""package {base_package}.main;

import {base_package}.main.proxy.CommonProxy;
import {base_package}.IModule;
import {base_package}.sundrugs.SunDrugs;
import {base_package}.sunshine.init.SunDynamX;
import {base_package}.sunshine.proxy.common.CommonProxy;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.SidedProxy;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;

import java.util.Arrays;

@Mod(modid = Constant.MODID, name = Constant.NAME, version = Constant.VERSION, dependencies = "before: dynamxmod")
public class Main {{

    public static final IModule[] MODULES = {{
            //new Module()
    }};

    @Mod.Instance
    public static Main instance;

    @SidedProxy(clientSide = "{base_package}.main.proxy.client.ClientProxy", serverSide = "{base_package}.main.proxy.server.ServerProxy")
    public static CommonProxy proxy;

    public static IModule[] getModules() {{
        return Arrays.stream(MODULES).filter(IModule::isEnabled).toArray(IModule[]::new);
    }}

    @Mod.EventHandler
    public void preInit(FMLPreInitializationEvent event) {{

        for (IModule modules : getModules()) {{
            modules.preInit(event);
        }}

        proxy.preInit(event);
    }}

    @Mod.EventHandler
    public void init(FMLInitializationEvent event) {{

        for (IModule modules : getModules()) {{
            modules.init(event);
        }}

        proxy.init(event);

    }}

    @Mod.EventHandler
    public void postInit(FMLPostInitializationEvent event) {{

        for (IModule modules : getModules()) {{
            modules.postInit(event);
        }}

        proxy.postInit(event);
    }}

    @Mod.EventHandler
    public void serverInit(FMLServerStartingEvent event) {{

        for (IModule modules : getModules()) {{
            modules.serverInit(event);
        }}

        proxy.serverInit(event);
    }}
}}
"""

def generate_mcmeta_class(info):
    base_package = info['package']  # ex: fr.alouchi.monmod

    return f"""{{
    "pack": {{
        "description": "examplemod resources",
        "pack_format": 3,
        "_comment": "A pack_format of 3 should be used starting with Minecraft 1.11. All resources, including language files, should be lowercase (eg: en_us.lang). A pack_format of 2 will load your mod resources with LegacyV2Adapter, which requires language files to have uppercase letters (eg: en_US.lang)."
    }}
}}
"""

def generate_module_class(info):
    base_package = info['package']  # ex: fr.alouchi.monmod

    return f"""import net.minecraft.command.ICommand;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;

public interface IModule {{
    void preInit(FMLPreInitializationEvent event);
    void init(FMLInitializationEvent event);
    void postInit(FMLPostInitializationEvent event);
    void serverInit(FMLServerStartingEvent event);

    boolean isEnabled();

    default void registerEvent(Object event) {{
        MinecraftForge.EVENT_BUS.register(event);
    }}

    default void registerCommand(ICommand command, FMLServerStartingEvent event) {{
        event.registerServerCommand(command);
    }}
}}
"""

def generate_bgradle_class(info):
    base_package = info['package']

    return f"""

buildscript {{
    repositories {{
        maven {{ url = 'https://maven.minecraftforge.net/' }}
        mavenCentral()
    }}
    dependencies {{
        classpath group: 'net.minecraftforge.gradle', name: 'ForgeGradle', version: '5.1.+', changing: true
        classpath 'com.github.jengelman.gradle.plugins:shadow:4.0.4'
    }}
}}

plugins {{
    id 'com.github.johnrengelman.shadow' version '4.0.4'
}}

repositories {{
    maven {{ url = 'https://repo.spongepowered.org/maven' }}

    maven {{
        url "https://cursemaven.com"
    }}

    flatDir {{
        dir 'libs'
    }}
}}

apply plugin: 'net.minecraftforge.gradle'
apply plugin: 'com.github.johnrengelman.shadow'
apply plugin: 'idea'

tasks.withType(JavaCompile) {{
    options.encoding = "UTF-8"
}}

version = '1.0.0'
group = '{base_package}'

sourceCompatibility = targetCompatibility = compileJava.sourceCompatibility = compileJava.targetCompatibility = '1.8'

minecraft {{
    mappings channel: 'stable', version: '39-1.12'

    runs {{
        client {{
            workingDirectory project.file('run')
            property 'forge.logging.markers', 'SCAN,REGISTRIES,REGISTRYDUMP'
            property 'forge.logging.console.level', 'debug'
        }}

        server {{
            property 'forge.logging.markers', 'SCAN,REGISTRIES,REGISTRYDUMP'
            property 'forge.logging.console.level', 'debug'
        }}
    }}
}}

jar {{
    duplicatesStrategy 'exclude'
}}

dependencies {{
    minecraft 'net.minecraftforge:forge:1.12.2-14.23.5.2860'
    implementation ("net.minecraftforge:mergetool:0.2.3.3") {{ force = true }}
    implementation fileTree(dir: 'libs', include: '*.jar')

    implementation 'org.json:json:20210307'

    shadow implementation('mysql:mysql-connector-java:8.0.33')

    compileOnly 'org.projectlombok:lombok:1.18.22'
    annotationProcessor 'org.projectlombok:lombok:1.18.22'
}}

configurations {{
    shadow
    compile.extendsFrom shadow
    shadowMe {{ transitive = false }}
}}

tasks.processResources {{
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}}

shadowJar {{
    classifier 'shadow'
    project.configurations.shadow.setTransitive(true)
    duplicatesStrategy 'exclude'
    configurations = [project.configurations.shadow]
    relocate 'org.apache.commons.collections4', 'com.station4.repack.org.apache.commons.collections4'
    relocate 'org.apache.http.client', 'com.station4.repack.org.apache.http.client'
    relocate 'gnu.trove', 'com.station4.repack.gnu.trove'
    relocate "com.neovisionaries.ws.client", "com.station4.repack.com.neovisionaries.ws.client"
    relocate "com.iwebpp.crypto", "com.station4.repack.com.iwebpp.crypto"
    relocate "com.google.gson", "com.station4.repack.com.google.gson"
    relocate "com.fasterxml.jackson", "com.station4.repack.com.fasterxml.jackson"
    relocate "okio", "com.station4.repack.okio"
    relocate "okhttp3", "com.station4.repack.okhttp3"
    relocate "okhttp3", "com.station4.repack.okhttp3"
    relocate "org.slf4j", "com.station4.repack.org.slf4j"
}}

build.dependsOn shadowJar
reobf {{
    shadowJar {{}}
}}

jar.finalizedBy('reobfJar')

/** Shit that idea needs to process resources ? **/
idea {{
    module {{
        inheritOutputDirs = true
    }}
}}
subprojects {{
    apply plugin: 'idea'
}}
task prepareAssets(type: Copy) {{
    group = 'build'
    from project.file('src/main/resources')
    into project.file('build/classes/java/main')
}}

classes.dependsOn(prepareAssets)

sourceSets.main.resources {{ srcDir 'src/main/resources' }}
"""

def generate_reference_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""package {base_package};

public class Reference {{
    public static final String MOD_ID = "{modid}";
    public static final String MOD_NAME = "{mod_name}";
    public static final String MOD_VERSION = "1.0.0";
    public static final String CLIENT_PROXY_CLASS = "{base_package}.main.proxy.ClientProxy";
    public static final String SERVER_PROXY_CLASS = "{base_package}.main.proxy.CommonProxy";
    public static final String MOD_ACCEPTED_VERSIONS = "[1.12.2]";
}}
"""

def generate_mcmod_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']
    desc = info['description']
    auth = info['author']

    return f"""[
{{
  "modid": "{modid}",
  "name": "{mod_name}",
  "description": "{desc}",
  "version": "${{version}}",
  "mcversion": "${{mcversion}}",
  "url": "",
  "updateUrl": "",
  "authorList": ["{auth}"],
  "credits": "@ModBase Generator - By Alouchi",
  "logoFile": "",
  "screenshots": [],
  "dependencies": []
}}
]
"""

def generate_client_proxy_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""package {base_package}.main.proxy.client;

import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.relauncher.Side;

public class ClientProxy extends CommonProxy {{
    @Override
    public void preInit(FMLPreInitializationEvent event) {{
    }}

    @Override
    public void init(FMLInitializationEvent event) {{
        //registerEvent(RegistryHandler.class);
    }}

    @Override
    public void postInit(FMLPostInitializationEvent event) {{

    }}
}}
"""

def generate_common_proxy_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""package {base_package}.main.proxy.common;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.event.FMLServerStartingEvent;

public abstract class CommonProxy {{
    public abstract void preInit(FMLPreInitializationEvent event);
    public abstract void init(FMLInitializationEvent event);
    public abstract void postInit(FMLPostInitializationEvent event);
    public void serverInit(FMLServerStartingEvent event) {{}};

    public void registerEvent(Object event) {{
        MinecraftForge.EVENT_BUS.register(event);
    }}
}}
"""

def generate_server_proxy_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""package {base_package}.main.proxy.server;

import {base_package}.main.proxy.common.CommonProxy;
import net.minecraftforge.fml.common.event.FMLInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPostInitializationEvent;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;

public class ServerProxy extends CommonProxy {{
    @Override
    public void preInit(FMLPreInitializationEvent event) {{

    }}

    @Override
    public void init(FMLInitializationEvent event) {{

    }}

    @Override
    public void postInit(FMLPostInitializationEvent event) {{

    }}
}}
"""

def generate_gradlew_bat(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%"=="" @echo off
@rem ##########################################################################
@rem
@rem  Gradle startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
@rem This is normally unused
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if %ERRORLEVEL% equ 0 goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar


@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

:end
@rem End local scope for the variables with windows NT shell
if %ERRORLEVEL% equ 0 goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE% equ 0 set EXIT_CODE=1
if not ""=="%GRADLE_EXIT_CONSOLE%" exit %EXIT_CODE%
exit /b %EXIT_CODE%

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
"""

def generate_gradlew_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""#!/bin/sh

#
# Copyright © 2015-2021 the original authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

##############################################################################
#
#   Gradle start up script for POSIX generated by Gradle.
#
#   Important for running:
#
#   (1) You need a POSIX-compliant shell to run this script. If your /bin/sh is
#       noncompliant, but you have some other compliant shell such as ksh or
#       bash, then to run this script, type that shell name before the whole
#       command line, like:
#
#           ksh Gradle
#
#       Busybox and similar reduced shells will NOT work, because this script
#       requires all of these POSIX shell features:
#         * functions;
#         * expansions «$var», «${{var}}», «${{var:-default}}», «${{var+SET}}»,
#           «${{var#prefix}}», «${{var%suffix}}», and «$( cmd )»;
#         * compound commands having a testable exit status, especially «case»;
#         * various built-in commands including «command», «set», and «ulimit».
#
#   Important for patching:
#
#   (2) This script targets any POSIX shell, so it avoids extensions provided
#       by Bash, Ksh, etc; in particular arrays are avoided.
#
#       The "traditional" practice of packing multiple parameters into a
#       space-separated string is a well documented source of bugs and security
#       problems, so this is (mostly) avoided, by progressively accumulating
#       options in "$@", and eventually passing that to Java.
#
#       Where the inherited environment variables (DEFAULT_JVM_OPTS, JAVA_OPTS,
#       and GRADLE_OPTS) rely on word-splitting, this is performed explicitly;
#       see the in-line comments for details.
#
#       There are tweaks for specific operating systems such as AIX, CygWin,
#       Darwin, MinGW, and NonStop.
#
#   (3) This script is generated from the Groovy template
#       https://github.com/gradle/gradle/blob/HEAD/subprojects/plugins/src/main/resources/org/gradle/api/internal/plugins/unixStartScript.txt
#       within the Gradle project.
#
#       You can find Gradle at https://github.com/gradle/gradle/.
#
##############################################################################

# Attempt to set APP_HOME

# Resolve links: $0 may be a link
app_path=$0

# Need this for daisy-chained symlinks.
while
    APP_HOME=${{app_path%"${{app_path##*/}}"}}  # leaves a trailing /; empty if no leading path
    [ -h "$app_path" ]
do
    ls=$( ls -ld "$app_path" )
    link=${{ls#*' -> '}}
    case $link in             #(
      /*)   app_path=$link ;; #(
      *)    app_path=$APP_HOME$link ;;
    esac
done

# This is normally unused
# shellcheck disable=SC2034
APP_BASE_NAME=${{0##*/}}
APP_HOME=$( cd "${{APP_HOME:-./}}" && pwd -P ) || exit

# Use the maximum available, or set MAX_FD != -1 to use that value.
MAX_FD=maximum

warn () {{
    echo "$*"
}} >&2

die () {{
    echo
    echo "$*"
    echo
    exit 1
}} >&2

# OS specific support (must be 'true' or 'false').
cygwin=false
msys=false
darwin=false
nonstop=false
case "$( uname )" in                #(
  CYGWIN* )         cygwin=true  ;; #(
  Darwin* )         darwin=true  ;; #(
  MSYS* | MINGW* )  msys=true    ;; #(
  NONSTOP* )        nonstop=true ;;
esac

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar


# Determine the Java command to use to start the JVM.
if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        # IBM's JDK on AIX uses strange locations for the executables
        JAVACMD=$JAVA_HOME/jre/sh/java
    else
        JAVACMD=$JAVA_HOME/bin/java
    fi
    if [ ! -x "$JAVACMD" ] ; then
        die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
    fi
else
    JAVACMD=java
    which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
fi

# Increase the maximum file descriptors if we can.
if ! "$cygwin" && ! "$darwin" && ! "$nonstop" ; then
    case $MAX_FD in #(
      max*)
        # In POSIX sh, ulimit -H is undefined. That's why the result is checked to see if it worked.
        # shellcheck disable=SC3045
        MAX_FD=$( ulimit -H -n ) ||
            warn "Could not query maximum file descriptor limit"
    esac
    case $MAX_FD in  #(
      '' | soft) :;; #(
      *)
        # In POSIX sh, ulimit -n is undefined. That's why the result is checked to see if it worked.
        # shellcheck disable=SC3045
        ulimit -n "$MAX_FD" ||
            warn "Could not set maximum file descriptor limit to $MAX_FD"
    esac
fi

# Collect all arguments for the java command, stacking in reverse order:
#   * args from the command line
#   * the main class name
#   * -classpath
#   * -D...appname settings
#   * --module-path (only if needed)
#   * DEFAULT_JVM_OPTS, JAVA_OPTS, and GRADLE_OPTS environment variables.

# For Cygwin or MSYS, switch paths to Windows format before running java
if "$cygwin" || "$msys" ; then
    APP_HOME=$( cygpath --path --mixed "$APP_HOME" )
    CLASSPATH=$( cygpath --path --mixed "$CLASSPATH" )

    JAVACMD=$( cygpath --unix "$JAVACMD" )

    # Now convert the arguments - kludge to limit ourselves to /bin/sh
    for arg do
        if
            case $arg in                                #(
              -*)   false ;;                            # don't mess with options #(
              /?*)  t=${{arg#/}} t=/${{t%%/*}}              # looks like a POSIX filepath
                    [ -e "$t" ] ;;                      #(
              *)    false ;;
            esac
        then
            arg=$( cygpath --path --ignore --mixed "$arg" )
        fi
        # Roll the args list around exactly as many times as the number of
        # args, so each arg winds up back in the position where it started, but
        # possibly modified.
        #
        # NB: a `for` loop captures its iteration list before it begins, so
        # changing the positional parameters here affects neither the number of
        # iterations, nor the values presented in `arg`.
        shift                   # remove old arg
        set -- "$@" "$arg"      # push replacement arg
    done
fi


# Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

# Collect all arguments for the java command;
#   * $DEFAULT_JVM_OPTS, $JAVA_OPTS, and $GRADLE_OPTS can contain fragments of
#     shell script including quotes and variable substitutions, so put them in
#     double quotes to make sure that they get re-expanded; and
#   * put everything else in single quotes, so that it's not re-expanded.

set -- \
        "-Dorg.gradle.appname=$APP_BASE_NAME" \
        -classpath "$CLASSPATH" \
        org.gradle.wrapper.GradleWrapperMain \
        "$@"

# Stop when "xargs" is not available.
if ! command -v xargs >/dev/null 2>&1
then
    die "xargs is not available"
fi

# Use "xargs" to parse quoted args.
#
# With -n1 it outputs one arg per line, with the quotes and backslashes removed.
#
# In Bash we could simply go:
#
#   readarray ARGS < <( xargs -n1 <<<"$var" ) &&
#   set -- "${{ARGS[@]}}" "$@"
#
# but POSIX shell has neither arrays nor command substitution, so instead we
# post-process each arg (as a line of input to sed) to backslash-escape any
# character that might be a shell metacharacter, then use eval to reverse
# that process (while maintaining the separation between arguments), and wrap
# the whole thing up as a single "set" statement.
#
# This will of course break if any of these variables contains a newline or
# an unmatched quote.
#

eval "set -- $(
        printf '%s\n' "$DEFAULT_JVM_OPTS $JAVA_OPTS $GRADLE_OPTS" |
        xargs -n1 |
        sed ' s~[^-[:alnum:]+,./:=@_]~\\&~g; ' |
        tr '\n' ' '
    )" '"$@"'

exec "$JAVACMD" "$@"
"""

def generate_gradlew_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""# Sets default memory used for gradle commands. Can be overridden by user or command line properties.
# This is required to provide enough memory for the Minecraft decompilation process.
org.gradle.jvmargs = -Xmx3G

# Mod Information
mod_version = 1.0
maven_group = com.cleanroommc
archives_base_name = modid

# If any properties changes below this line, run `gradlew setupDecompWorkspace` and refresh gradle again to ensure everything is working correctly.

# Boilerplate Options
use_mixins = false
use_coremod = false
use_assetmover = false

# Access Transformer files should be in the root of `resources` folder and with the filename formatted as: `{{archives_base_name}}_at.cfg`
use_access_transformer = false

# Coremod Arguments
include_mod = true
coremod_plugin_class_name =
"""

def generate_gitignore_class(info):
    base_package = info['package']
    modid = info['modid']
    mod_name = info['mod_name']

    return f"""# eclipse
bin
*.launch
.settings
.metadata
.classpath
.project

# idea
out
*.ipr
*.iws
*.iml
.idea

# gradle
build
.gradle

# other
eclipse
run

# Files from Forge MDK
forge*changelog.txt
"""



if __name__ == "__main__":
    info = get_info()
    if info:
        create_mod_base(info)
