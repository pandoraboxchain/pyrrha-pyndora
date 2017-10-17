# @dev Since `destroyself()` zeroes values of all variables, we need the first state (corresponding to zero)
# to indicate that contract had being destroyed
DESTROYED = 0xFF

# @dev Reserved system state not participating in transition table. Since contract creation all variables are
# initialized to zero and contract state will be zero until it will be initialized with some definite state
UNINITIALIZED = 0

# @dev When node goes offline it can mark itself as offline to prevent penalties.
# If node is not responding to Pandora events and does not submit updates on the cognitive work in time
# then it will be penaltied and put into `Offline` state
OFFLINE = 1

# @dev Initial and base state
IDLE = 2

# @dev State when cognitive job is created and worker node is assigned to it, but the node didn't responded with
# readiness status yet
ASSIGNED = 3

# @dev Worker node have responded with readiness status and awaits cognitive job contract to transition into the
# next stage
READY_FOR_DATA_VALIDATION = 4

# @dev Worker node downloads and validates source data for correctness and consistency
VALIDATING_DATA = 5

# @dev Worker node have finished data validation, confirmed data correctness and completeness, and reported
# readiness to start performing actual cognition – however cognitive job contract didn't transitioned into
# cognitive state yet (not all workers have reported readiness)
READY_FOR_COMPUTING = 6

# @dev State when worker node performs cognitive job
COMPUTING = 7

# @dev Intermediary state when worker node stake is reduced below threshold required for performing
# cognitive computations
INSUFFICIENT_STAKE = 8

# @dev Intermediary state preventing from performing any type of work during penalty process
UNDER_PENALTY = 9


statuses = {
    "destroyed": DESTROYED,
    "uninitialized": UNINITIALIZED,
    "offline": OFFLINE,
    "idle": IDLE,
    "assigned": ASSIGNED,
    "ready_for_data_validation": READY_FOR_DATA_VALIDATION,
    "validating_data": VALIDATING_DATA,
    "ready_for_computing": READY_FOR_COMPUTING,
    "computing": COMPUTING,
    "insufficient_stake": INSUFFICIENT_STAKE,
    "under_penalty": UNDER_PENALTY,
}

def get_status_by_number(n):
    sbn = dict([(item[1], item[0]) for item in statuses.items()])
    return sbn[n]
