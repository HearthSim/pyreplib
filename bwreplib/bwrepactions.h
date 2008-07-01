//----------------------------------------------------------------------------------------------------
// Replay Actions - jca (May 2003)
//----------------------------------------------------------------------------------------------------
// Classes you should use:
//
// class BWrepActionList : list of all actions in the replay (given by the BWrepFile object)
// class BWrepAction     : generic action from the list
// class BWrepActionXXX  : specific class for a specific action (ex: BWrepActionSelect for a "select" action)
//----------------------------------------------------------------------------------------------------
#ifndef INC_BWREPACTIONS_H
#define INC_BWREPACTIONS_H

#include <assert.h>

//----------------------------------------------------------------------------------------------------

typedef const char *(pfnGetParameters)(const unsigned char *data, int datasize);

// any action
class BWrepAction
{
public:
	// action time (in "tick" units. Divide by 23 to get the approximate time in seconds. not very accurate)
	static const int m_timeRatio;//=23
	unsigned long GetTime() const {return m_time;}

	// action name
	const char *GetName() const;

	// action id (returns a eACTIONNAME from BWrepGameData.h)
	int GetID() const {return m_ordertype;}

	// player id (use BWrepHeader::getPlayer to get player name)
	int GetPlayerID() const {return (int)m_playerid;}

	// parameters as text
	const char *GetParameters() const;

	// pointer on parameters (must be casted to the correct BWrepActionXXX::Params)
	const void *GetParamStruct(int* pSize=0) const;

	// -internals used by BWrepActionList
	void Clear();
	void SetPlayerID(unsigned char playerid) {m_playerid=playerid;}
	void SetOrderType(unsigned char type) {m_ordertype=type;}
	void SetTime(unsigned long time) {m_time=time;}
	void SetData(class BWrepActionList *parent, unsigned long off) {m_parent=parent; m_dataoff=off;}

	// to associate user data with an action
	enum {MAXUSERDATA=2};
	void SetUserData(int idx, unsigned long data) {assert(idx<MAXUSERDATA); m_userdata[idx]=data;}
	unsigned long GetUserData(int idx) const {assert(idx<MAXUSERDATA); return m_userdata[idx];}

	// process an action
	bool ProcessActionParameters(const unsigned char * &current, int& read, unsigned char& size);

	//----was moved to class BWrepGameData
	// get action name from action id (action id is from eACTIONNAME)
	//static const char *GetActionNameFromID(int id);
private:
	class BWrepActionList *m_parent;
	unsigned long m_time;      // time value indicating offset from beginning of game
	unsigned char m_playerid;  // 1 byte player id found in the header in section 1	(=slot)
	unsigned char m_ordertype; // byte id of the type of order (ie select, move, build scv, upgrade the base, research siege mode, burrow, seige, ally chat, quit game, etc etc)
	unsigned long m_dataoff;   // offset to data bytes in data block
	int m_datasize;	// data size
	pfnGetParameters *m_pGetParamText; // pointer to function for extracting parameters

	unsigned long m_userdata[MAXUSERDATA];
};

//----------------------------------------------------------------------------------------------------

// decoded actions list (it's an array really)
class BWrepActionList
{
public:
	BWrepActionList() : m_actions(0), m_data(0), m_size(0), m_actionCount(0) {}
	~BWrepActionList();

	// get pointer on nth action
	const BWrepAction *GetAction(int i) const {return i<m_actionCount ? &m_actions[i] : 0;}

	// get action count
	int GetActionCount() const {return m_actionCount;}

	// -internal: decode all actions from an uncrompressed buffer
	bool DecodeActions(const unsigned char *buffer, int cmdSize, bool clear=true);
	const void *GetAbsAddress(unsigned long off) {return m_data+off;}
	void Sort();
private:
	// actions array
	BWrepAction *m_actions;
	// available size in array
	int m_size;
	// action count
	int m_actionCount;
	// pointer to uncompressed data for section 3
	unsigned char *m_data;     
	unsigned long m_datasize;

	// clear current action list
	void _Clear();

	// all actions for a same time tick
	bool AddAction(BWrepAction *action);
};

//----------------------------------------------------------------------------------------------------

// macro to declare a new action class
#define DECLAREACTION(classname)\
class BWrepAction##classname : public BWrepAction\
{\
public:\
	static const char * gGetParameters(const unsigned char *data, int datasize);\
	struct Params {

#define ENDDECL };};

// macro to declare an action without parameters
#define DECLAREACTION_NOPARAM(classname)\
class BWrepAction##classname : public BWrepAction\
{\
public:\
	static const char * gGetParameters(const unsigned char *data, int datasize);\

#define ENDDECL_NOPARAM };

#pragma pack(push, 1)

//----------------------------------------------------------------------------------------------------
// ALL KNOWN ACTIONS
//----------------------------------------------------------------------------------------------------

DECLAREACTION(Stop)
		unsigned char m_unknown;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Select)
		unsigned char m_unitCount;
		unsigned short m_unitid[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Deselect)
		unsigned char m_unitCount;
		unsigned short m_unitid[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(ShiftSelect)
		unsigned char m_unitCount;
		unsigned short m_unitid[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(ShiftDeselect)
		unsigned char m_unitCount;
		unsigned short m_unitid[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Train)
		unsigned short m_unitType;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Hatch)
		unsigned short m_unitType;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(CancelTrain)
		unsigned char m_unknown[2];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Move)
		unsigned short m_pos1;
		unsigned short m_pos2;
		unsigned short m_unitid;
		unsigned short m_unknown1;
		unsigned char m_unknown2;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Build)
		unsigned char m_buildingtype;
		unsigned short m_pos1;
		unsigned short m_pos2;
		unsigned short m_buildingid;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Research)
		unsigned char m_techid;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Upgrade)
		unsigned char m_upgid;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Lift)
		unsigned char m_unknown[4];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Attack)
		unsigned short m_pos1;
		unsigned short m_pos2;
		unsigned short m_unitid;
		unsigned short m_unknown1;
		unsigned char m_type;
		unsigned char m_modifier;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Ally)
		unsigned char m_unknown[4];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Vision)
		unsigned char m_unknown[2];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(HotKey)
		unsigned char m_type;
		unsigned char m_slot;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(HoldPosition)
		unsigned char m_unknown;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Cloak)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Decloak)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Siege)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Unsiege)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(Cancel)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(CancelNuke)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(CancelHatch)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(CancelResearch)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(Stimpack)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(BuildInterceptor)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(MergeArchon)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION_NOPARAM(MergeDarkArchon)
ENDDECL_NOPARAM

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Unload)
		unsigned char m_unknown[2];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(UnloadAll)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(ReturnCargo)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(LeftGame)
		unsigned char m_how;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Morph)
		unsigned short m_buildingid;
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Burrow)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Unburrow)
		unsigned char m_unknown[1];
ENDDECL

//----------------------------------------------------------------------------------------------------

DECLAREACTION(Unknown)
		unsigned char m_unknown[1];
ENDDECL

#pragma pack(pop)

//----------------------------------------------------------------------------------------------------

#endif // INC_BWREPACTIONS_H
