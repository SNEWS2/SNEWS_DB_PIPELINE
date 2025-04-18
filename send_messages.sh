#!/bin/bash

snews_pt set-name -n DUNE 
snews_pt publish ../SNEWS_Publishing_Tools/snews_pt/test/example_coincidence_tier_message.json --firedrill
snews_pt publish ../SNEWS_Publishing_Tools/snews_pt/test/example_heartbeat_message.json --firedrill
snews_pt publish ../SNEWS_Publishing_Tools/snews_pt/test/example_significance_tier_message.json --firedrill
