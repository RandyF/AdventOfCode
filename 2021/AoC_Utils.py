#==============================================================================
# Debug Level Constants
#==============================================================================
DBG_MAJOR = 1
DBG_MAJOR_DETAIL = 2
DBG_MAJOR_START = 3

DBG_MINOR = 4
DBG_MINOR_DETAIL = 5
DBG_MINOR_START = 6

DBG_STATE = 7
DBG_STATE_DETAIL = 8
DBG_STATE_START = 9

DBG_FINE_DETAIL = 10
DBG_ULTRA_DETAIL = 11
DBG_MEGA_DETAIL = 12

#==============================================================================
# debug() function - controllable display print()
#
# This extends print() with two more keyword arguments:
#   DebugLevel - Verbosity of which this function will print output
#   Verbocity - Current Verbosity Level
#==============================================================================
def debug(*args,**kwargs): 

    # Get current DebugLevel
    if 'DebugLevel' in kwargs:
        tDebugLevel = kwargs['DebugLevel']
        #print("Got DebugLevel", tDebugLevel )
        del kwargs['DebugLevel']
    elif 'DefaultDebugLevel' in globals():
        tDebugLevel = DefaultDebugLevel
    else:
        tDebugLevel = 0 

    # Get current Verbosity
    if 'Verbosity' in kwargs:
        tVerbosity = kwargs['Verbosity']
        #print("Got Verbosity", tVerbosity )
        del kwargs['Verbosity']
    elif 'DefaultGlobalVerbosity' in globals():
        tVerbosity = DefaultGlobalVerbosity
    else:
        tVerbosity = 10**99
    
    #print Output if Verbosity is greater-than-equal to Debug Level
    if tDebugLevel <= tVerbosity:
        print(*args,**kwargs)