import os
import sys
import json
import psutil
import discord
import subprocess
from colorama import Fore, Back
from colorama import init as colorama_init

#======================================================
# Messages used on this script, Feel free to add more languages
#======================================================
__dict_messages__ = {
    "configuration.is.found":
    {
        "spanish": "{}Usar configuración actual\n{}Configurar de nuevo\nConfiguración actual:\n{}{}",
        "english": "{}Use current configuration\n{}Configure again\nCurrent configuration:\n{}{}",
    },
    "configuration.is.not.found":
    {
        "spanish": "No se pudo encontrar una configuracion en {}\nVamos a configurar la aplicación.",
        "english": "Can not locate configuration file at {}\nLets configure the application.",
    },
    "configuration.skip":
    {
        "spanish": "{}Usar valor actual \"{}\"",
        "english": "{}Use current value \"{}\"",
    },
    "configuration.wrong":
    {
        "spanish": "{}El valor otorgado es invalido \"{}\"",
        "english": "{}The provided value is invalid \"{}\"",
    },
    "configuration.token":
    {
        "spanish": "Inserta el token de tu aplicación BOT de discord.",
        "english": "Insert your discord's application BOT token.",
    },
    "configuration.server":
    {
        "spanish": "Inserta el ID de tu servidor de discord.",
        "english": "Insert the discord server's ID.",
    },
    "configuration.hlds":
    {
        "spanish": "Inserta la ruta absoluta a hlds.exe por ejemplo: C:/Program Data/../Half-Life/hlds.exe",
        "english": "Insert the absolute path to hlds.exe for example: C:/Program Data/../Half-Life/hlds.exe",
    },
    "configuration.roles":
    {
        "spanish": "Inserta una lista de ID de roles de discord que podrán utilizar el comando. Separa con espacios. Usa 0 para no limitar a ningun usuario. Usa -1 para solo administradores.",
        "english": "Insert a list of discord roles's ID that would be able to use the command. Separate with spaces. Use 0 to not limit to any user. Use -1 for administrators only.",
    },
    "configuration.arguments":
    {
        "spanish": "Inserta una lista de argumentos para ejecutar en el hlds.exe",
        "english": "Insert a list of arguments to execute on the hlds.exe",
    },
    "starting.program":
    {
        "spanish": "Iniciando programa con la configuracion:\n{}{}",
        "english": "Starting program with configuration:\n{}{}",
    },
    "start.bot":
    {
        "spanish": "Bot conectado como \"{}\"",
        "english": "Bot connected as \"{}\"",
    },
    "command.running":
    {
        "spanish": "El servidor esta actualmente corriendo.",
        "english": "The server is actually running.",
    },
    "command.run":
    {
        "spanish": "Iniciando servidor.",
        "english": "Initiating server.",
    },
    "command.no.administrator":
    {
        "spanish": "Este comando ha sido configurado como solo para administradores.",
        "english": "This command is been configured as for administrators only.",
    },
    "command.no.roles":
    {
        "spanish": "Este comando ha sido configurado como solo para roles especificos.",
        "english": "This command is been configured as for specific roles only.",
    },
};

global app_name;
app_name = 'hl-server-manager';

global cfg;
cfg = {};

#======================================================
# Various utility
#======================================================
def __language__() -> str:

    import locale;

    __syslang__ = locale.getlocale();

    __lang__ = __syslang__[ 0 ];

    if __lang__.find( '_' ) != -1:

        __lang__ = __lang__[ 0 : __lang__.find( '_' ) ];

    return str( __lang__.lower() );

#======================================================

def printf( data: str, arguments: list[str] = [], dont_print: bool = False, dont_color: bool = False ) -> str:

    __data__ = __dict_messages__[data];

    __string__ = __data__.get( __language__, __data__.get( 'english', '' ) );

    for __arg__ in arguments:

        __string__ = __string__.replace( "{}", str( __arg__ ), 1 );

    __printf__ = f'{Back.WHITE}{Fore.BLACK}{__string__}{Back.RESET}{Fore.RESET}\n' if not dont_color else f'{__string__}\n';

    __result__ = None;

    if not dont_print:

        print(__printf__);

    return __printf__;

#======================================================
# Setups
#======================================================

def get_config_path() -> list[str]:

    __appdata_path__ = os.getenv( "APPDATA" );

    __app_folder__ = os.path.join( __appdata_path__, app_name );

    __config_path__ = os.path.join( __app_folder__, "config.json" );

    __dirs__ = [ __config_path__, __app_folder__, __appdata_path__ ];

    return __dirs__;

def get_config() -> None:

    __path__ = get_config_path();

    __data__ = {};

    if os.path.exists( __path__[0] ):

        with open( __path__[0], 'r' ) as __config__:

            __data__ = json.load( __config__ );

            __config__.close();

    global cfg;
    cfg = __data__;

def set_config() -> None:

    __path__ = get_config_path();

    os.makedirs( __path__[1], exist_ok=True );

    with open( __path__[0], 'w' ) as __config__:

        global cfg;
        json.dump( cfg, __config__, indent=4 );

def configuration( update: bool = False ) -> None:

    global cfg;

    def __rc__( var: str, enforce: bool = False ) -> None:

        os.system( 'cls' );

        printf( 'configuration.{}'.format( var ), [] );

        if enforce:

            printf( "configuration.wrong", [ Back.RED, cfg.get( var ) ] );

        elif var in cfg:

            printf( "configuration.skip", [ "1 - ", cfg.get( var ) ] );

        __input__ = input();

        if not __input__.isnumeric() or __input__.isnumeric() and int(__input__) != 1:
    
            cfg[ var ] = __input__;

    __rc__( "token" );
    __rc__( "server" );
    __rc__( "hlds" );
    while not os.path.exists( cfg.get( "hlds", '' ) ):
        __rc__( "hlds", True );
    __rc__( "roles" );
    __rc__( "arguments" );

    set_config();

#======================================================
# Bot
#======================================================

# https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
class Bot( discord.Client ):

    def __init__( self, *, intents: discord.Intents ):

        super().__init__( intents=intents );

        self.tree = discord.app_commands.CommandTree( self );

    async def setup_hook(self):

        __MY_GUILD__ = discord.Object( id = int( cfg[ "server" ] ) );

        self.tree.clear_commands( guild=__MY_GUILD__ );

        self.tree.copy_global_to( guild=__MY_GUILD__ );

        await self.tree.sync( guild=__MY_GUILD__ );

# Initialise as None because cfg may not be ready yet.
global bot;
bot: discord.Client | Bot = None;

def init_bot() -> None:

    global bot;
    bot = Bot( intents=discord.Intents.all() );

def await_input() -> None:

    if not "-bg" in sys.argv:

        get_config();

        global cfg;

        if len(cfg) == 0:

            printf( "configuration.is.not.found", [ get_config_path()[0] ] );

            configuration();

        else:

            __input__ = '';

            while not __input__.isnumeric() or not int(__input__) in [ 1, 2 ]:

                os.system( 'cls' );

                printf( "configuration.is.found", [ "1 - ", "2 - ", Back.GREEN, json.dumps( cfg, indent=4 ) ] );

                __input__ = input();

            if int(__input__) == 2:

                configuration(True);

        os.system( 'cls' );

        printf( "starting.program", [ Back.GREEN, json.dumps( cfg, indent=4 ) ] );

    else:

        get_config();

        if len(cfg) == 0:

            exit(1);

    init_bot();

colorama_init();

await_input();

@bot.tree.command()
async def server_start( interaction: discord.Interaction ):
    """Starts the server"""

    await interaction.response.defer( thinking=True );

    try:

        if int(cfg.get("roles",0)) == -1 and not interaction.user.guild_permissions.administrator:

            await interaction.followup.send( content=printf( "command.no.administrator", dont_print=True, dont_color=True ) );

            return;

        elif "roles" in cfg and cfg["roles"] != '0':

            breturn = True;

            roles = cfg["roles"].split(" ");

            for role in roles:

                role = role.strip();

                if role and role != '' and role.isnumeric():

                    if interaction.user.get_role( int(role) ):

                        breturn = False;
        
            if breturn:

                await interaction.followup.send( content=printf( "command.no.roles", dont_print=True, dont_color=True ) );

                return;

        for process in psutil.process_iter( [ 'name' ] ):

            if process.info[ 'name' ].lower() == cfg["hlds"][ cfg["hlds"].replace('\\', '/').rfind('/') + 1 : ].lower():

                await interaction.followup.send( content=printf( "command.running", dont_print=True, dont_color=True ) );
    
                return;

        await interaction.followup.send( content=printf( "command.run", dont_print=True, dont_color=True ) );

        subprocess.Popen( '{} {}'.format( cfg[ "hlds" ], cfg[ "arguments" ] ), shell=True, cwd=os.path.dirname( cfg["hlds"] ) );

    except Exception as e:

        await interaction.followup.send( "Exception:\n```\n{}```".format( e ) );

@bot.event
async def on_ready():

    await bot.wait_until_ready();

    printf( "start.bot", [ bot.user.name ] );

bot.run( cfg[ "token" ] );
