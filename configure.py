# set mode PVE EVE PVP
mode = 'PVE'

# pve mode config
if mode == 'PVE':
    HUMAN_COLOR = 'BLACK'
    AI_STRATEGY = 'MODEL'
if mode == 'EVE':
    BLACK_AI_STRATEGY = 'MODEL'
    WHITE_AI_STRATEGY = 'RANDOM'
