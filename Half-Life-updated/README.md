Include header and source in your project.


Go to client.cpp
```cpp
#include "hl-server-manager"
```

Scroll down to
```cpp
//
// GLOBALS ASSUMED SET:  g_ulFrameCount
//
void StartFrame()
{
	if (g_pGameRules)
		g_pGameRules->Think();

	if (g_fGameOver)
		return;
...
....
}
```

Call our think function after with the initialised gamerules
```cpp
void StartFrame()
{
	g_Server.RunFrame();

	if (g_pGameRules)
	{
		g_pGameRules->Think();
    	hl_ServerManager.Think();
	}

	if (g_fGameOver)
		return;
...
....
}
```

Alternatively go to game.cpp and register a new cvar for controling in seconds the ratetime for writing the file
```cpp
cvar_t sv_manager_write_ratetime = {"sv_manager_write_ratetime", "10", FCVAR_SERVER};

...
....

// Register your console variables here
// This gets called one time when the game is initialied
void GameDLLInit()
{
	...
	....

	CVAR_REGISTER(&sv_manager_write_ratetime);
}
```

Now compile your serverdll.

[Here](https://github.com/Mikk155/halflife-updated/tree/hl-server-manager)'s a branch with this sole implementation.
