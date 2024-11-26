/***
 *
 *	Copyright (c) 1996-2001, Valve LLC. All rights reserved.
 *
 *	This product contains software technology licensed from Id
 *	Software, Inc. ("Id Technology").  Id Technology (c) 1996 Id Software, Inc.
 *	All Rights Reserved.
 *
 *   Use, distribution, and modification of this source code and/or resulting
 *   object code is restricted to non-commercial enhancements to products from
 *   Valve LLC.  All other use, distribution, or modification is prohibited
 *   without written permission from Valve LLC.
 *
 ****/

#include "hl-server-manager.h"

void MyServerManager::Think()
{
    if( !g_pGameRules->IsMultiplayer() || !IS_DEDICATED_SERVER() || flLastThink > gpGlobals->time )
        return;

    if( !init )
    {
        snprintf( filename, sizeof(filename), "%s/scripts/store/hl-server-manager.json", FileSystem_GetModDirectoryName().c_str() );
        UTIL_LogPrintf( "[Debug] hl-server-manager: Initialised filename path \"%s\"\n", filename );
        init = true;
    }

    auto writefile = []( int seconds, const char* filename ) -> float
    {
        std::ofstream file( filename );

        if( file.is_open() )
        {
            file << "{\"seconds\": " << seconds << "}";
            file.close();
        }
        else
        {
    		UTIL_LogPrintf( "[Error] hl-server-manager: Failed to open file \"%s\" a delay may occur in python.\n", filename );
            return gpGlobals->time + 0.1f;
        }

        float fCooldown = CVAR_GET_FLOAT( "sv_manager_write_ratetime" );

        return gpGlobals->time + ( fCooldown > 0 ? fCooldown : 10.0f );
    };

	CBaseEntity* player = UTIL_FindEntityByClassname( NULL, "player" );

    if( player && player != nullptr )
    {
        if( seconds != 0 )
        {
            seconds = 0;

            if( flWriteTime <= gpGlobals->time )
                flWriteTime = writefile(seconds, filename);
        }
        seconds = 0;
    }
    else
    {
        seconds++;

        if( flWriteTime <= gpGlobals->time )
            flWriteTime = writefile(seconds, filename);
    }

    flLastThink = gpGlobals->time + 1.0f;
}
