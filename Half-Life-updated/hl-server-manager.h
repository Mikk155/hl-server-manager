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

#include <fstream>

#include "extdll.h"
#include "util.h"
#include "const.h"
#include "gamerules.h"
#include "filesystem_utils.h"

#pragma once

class MyServerManager final
{
	public:
		void Think();

	private:
        bool init = false;
        int seconds = 0;
        char filename[_MAX_PATH + 1];
        float flLastThink = 0.0f;
        float flWriteTime = 0.0f;
};

inline MyServerManager hl_ServerManager;
