/*
	"plugin"
	{
		"name" "hl-server-manager"
		"script" "hl-server-manager"
		"concommandns" "plrmgr"
	}
*/

MyServerManager@ hl_ServerManager;

void PluginInit()
{
	g_Module.ScriptInfo.SetAuthor( "Mikk" );
	g_Module.ScriptInfo.SetContactInfo( "https://github.com/Mikk155/hl-server-manager" );
	MapInit();
}


void MapInit()
{
	@hl_ServerManager = null;
	@hl_ServerManager = MyServerManager();

	if( hl_ServerManager is null )
	{
		g_Logger.error( "Couldn't instantiate a schedule pointer." );
	}
}

Logger g_Logger;
class Logger
{
	private string log( string message, array<string> arguments = {} )
	{
		for( uint ui = 0; ui < arguments.length(); ui++ )
		{
			const size_t size = message.Find( "{}", 0, String::DEFAULT_COMPARE );

			if( size != String::INVALID_INDEX )
			{
				message = message.SubString( 0, size ) + arguments[ui] + message.SubString( size + 2 );
			}
			else
			{
				break;
			}
		}
		return " hl-server-manager: " + message + "\n";
	}

	void error( string message, array<string> arguments = {} )
	{
		g_EngineFuncs.ServerPrint( "[Error]" + this.log( message, arguments ) );
	}

	void warn( string message, array<string> arguments = {} )
	{
		g_Game.AlertMessage( at_console, "[Debug]" + this.log( message, arguments ) );
	}

	void debug( string message, array<string> arguments = {} )
	{
		g_Game.AlertMessage( at_aiconsole, "[Debug]" + this.log( message, arguments ) );
	}
}

final class MyServerManager
{
	private int seconds = 0;
	private CScheduledFunction@ schedule = null;

	bool enabled()
	{
		return ( schedule !is null );
	}

	~MyServerManager()
	{
		this.remove();
	}

	MyServerManager()
	{
		this.init();
	}

	void init()
	{
		@schedule = g_Scheduler.SetInterval( @this, "checker", 1.0f, g_Scheduler.REPEAT_INFINITE_TIMES );
	}

	void remove()
	{
		if( enabled() )
		{
			g_Scheduler.RemoveTimer( @schedule );
			@schedule = null;
		}

		g_Scheduler.ClearTimerList();
	}

	void checker()
	{
		this.seconds++;

		if( g_PlayerFuncs.GetNumPlayers() != 0 )
		{
			this.seconds = 0;
		}

		File@ pFile = g_FileSystem.OpenFile( "scripts/plugins/store/hl-server-manager.json", OpenFile::WRITE );

		if( pFile is null || !pFile.IsOpen() )
		{
			g_Logger.error( "Couldn't create cache file." );
			return;
		}

		pFile.Write( "{
	\"seconds\": "+string(this.seconds)+"
}" );
	}
}
