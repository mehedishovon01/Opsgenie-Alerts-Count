import sys
import time
import pandas as pd
from datetime import datetime
from collections import Counter

# Read from Opsgenie Exported Data with 5 Columns
col_list = ["Message", "Status", "Acknowledged", "CreatedAtDate", "Owner"]
df = pd.read_csv("finalAlertData.csv", usecols=col_list)

# Convert to List
convert_to_list = df.values.tolist()

# Alerts date between and Decoration
# Start Date
end_line = convert_to_list[-1][3]
end_str = end_line.split(' ')
start_date = end_str[0]

# End Date
start_line = convert_to_list[0][3]
start_str = start_line.split(' ')
end_date = start_str[0]

# Get human readable time for file nameing
dt = datetime.strptime(start_date, "%Y/%m/%d")
dt_end = datetime.strptime(end_date, "%Y/%m/%d")
month = f"{dt.strftime('%B')}"
startDate = f"{dt.strftime('%d')}"
endDate = f"{dt_end.strftime('%d')}"

# Store the original sys.stdout
original_stdout = sys.stdout

# Redirect stdout to a text file exporting
sys.stdout = open(f'{month}_({startDate}_to_{endDate}).txt', "w")

# Print Authorised By Mulytic with date between and Decoration
print('''/*
*
* @Mulytic Energy Solutions LTD.
*
* Alerts Between {} to {}
*/
'''.format(start_date, end_date))


# Filter out Owner of Alerts
owner_mulytic = 0
not_owner_mulytic = 0

# Mulytic Owned Alerts & Mulytic Not Owned Alerts
for alert in convert_to_list:
    if (alert[4] == 'support@mulytic.io' or alert[4] == 'progga.roy@mulytic.io'):
        owner_mulytic += 1
    elif (alert[4] != 'support@mulytic.io' or alert[4] != 'progga.roy@mulytic.io'):
        not_owner_mulytic += 1

# Make a list for Printable Format
alerts_distribute_table = [
    ['Total Number of Alerts                ', len(convert_to_list)],
    ['____________________________________________________', ''],
    ['Mulytic Not Owned                     ', not_owner_mulytic],
    ['Mulytic Owned                         ', owner_mulytic]
    ]

# Print all data
for row in alerts_distribute_table:
    print('{:1} {:^12}'.format(*row))

# Find out all Acknowledgement Alerts by Mulytic
print(f"\n" * 3 + "=" * 70 + " All Acknowledgement Alerts by Mulytic " + "=" * 70 + "\n")

# Total Alerts
all_ack_alerts = []
alert_count = 0

# Filter out Acknowledgement & Mulytic Owened Alerts
for alert in convert_to_list:
    if alert[2] == True and (alert[4] == 'support@mulytic.io' or alert[4] == 'progga.roy@mulytic.io'):
        all_ack_alerts.append(alert)
        alert_count = alert_count + 1

print('Total Acknowledgement Alerts ~~~~~~~~~~~> ' + str(alert_count))

# !!! `charging` alerts list with a title. Pass this two list into the main function
charging_list = [
    ['Controller', 'offline (last seen at'],
    ['Controller', 'chargers in error or offline']
]
charging_title = (f"\n" * 3 + "~" * 60 + " Charging (Controller & Chargers/Connectors) " + "~" * 67 + "\n")

# !!! `german grid` alerts list with a title. Pass this two list into the main function
de_alerts = [
    ['de_amp_coulomb', 'is under required power'],
    ['de.amprion', 'is under required power'],
    ['[Q_TE_A_WEST_REMONDIS_', 'SOCs above max healthy SOC above threshold!'],
    ['[Q_TE_A_WEST_REMONDIS_', 'ESS SOCs below min healthy SOC above threshold!'],
    ['[Q_TE_A_WEST_ENERVIEV_ELV_', 'SOCs above max healthy SOC above threshold!'],
    ['[Q_TE_A_WEST_ENERVIEV_ELV_', 'ESS SOCs below min healthy SOC above threshold!'],
    ['[Q_TE_A_WEST_REMONDIS_', 'FCR power 0 events over threshold!'],
    ['[Q_TE_A_WEST_ENERVIEV_ELV_', 'FCR power 0 events over threshold!'],
    ['Requested FCR power is zero for', 'de_amprion'],
    ['Backup is active for', 'de_amprion'],
    ['External backup required for de_amprion'],
    ['ESS power response metrics'],
    ['General error safety contact',],
    ['AC grid undervoltage shutdown'],
    ['AC grid overvoltage shutdown']
]
fire_alarts = [
    ['Facility: Fire detection triggered'],
    ['Facility: Fire detection system not available'],
    ['Facility: Grid- and system protection triggered'],
    ['Facility: Power failure'],
    ['Emergency Stop triggered for this system']
]
critical_storage = [
    ['DC source missing', 'undervoltage intermediate circuit'],
    ['kill-switch tripped'],
    ['Inverter 2 Inverter: Master contactor stuck'],
    ['Master contactor stuck battery unit'],
    ['Discrepancy error master'],
    ['Isolation faulty'],
    ['Isolation critical'],
    ['Communication timeout'],
    ['Converter general error'],
    ['Max SOC exceeded'],
    ['Breaker tripped'],
    ['Overvoltage DC'],
    ['Overvoltage intermediate circuit'],
    ['Max', 'current exceeded'],
    ['Max frequency exceeded'],
    ['Min Frequency fallen below'],
    ['Temperature sensor fault'],
    ['Transmission error transducer'],
    ['Alive error'],
    ['Filter charge contactor stuck'],
    ['Battery CAN connexion failure'],
    ['AC gird overload']
]

german_grid = (
    de_alerts, 
    fire_alarts,
    critical_storage
)
de_title = (f"\n" * 3 + "~" * 75 + " German Grid (DE Grid) " + "~" * 80 + "\n")


# !!! `amsterdam` alerts list with a title. Pass this two list into the main function
amsterdam_grid_alerts = [
    ['PRL Power Error The amount of power the storage can supply is lower than the maximum FCR power it is supposed t'],
    ['Relay cannot reach the unit for nl_tennet Problem with the unitset described. Check Dashboards'],
    ['Requested FCR power is zero for nl_tennet'],
    ['Storage Control Storage status error Storage status error. Storage is in a state other than 100 - run or 50 -'],
    ['Storage Control Lost connection to storage System not alive. Storage is not responding to communication.'],
    ['Critical storage error The storage system reports a critical storage error. Please contact the hardware supplie'],
    ['Storage power response incorrect Storage is not responding to power requests correctly'],
    ['Storage System Error', 'Please call Eaton if this persists']
]
aa_title = (f"\n" * 3 + "~" * 71 + " Amsterdam Grid (AA Grid) " + "~" * 75 + "\n")


# !!! `tokai 1 douai` alerts list with a title. Pass this two list into the main function
douai_controller = [
    ['fr_rte_tokai1_douai: is under required power Problem with the unitset described'],
    ['Tokai1_Douai', 'FCR power 0 events over threshold!'],
    ['Tokai1_Douai', 'has not changed frequency for 5min'],
    ['has lost connection', '156832d4fd59f644db62c98f9877bd54'],
    ['has lost connection', '124ea21a09aaaf34607e9aaa2cc36c53'],
    ['has lost connection', 'a40222bd7b99ebc06a8d935b3a26fce3'],
    ['has lost connection', 'e4110f1463cbc5f40d485428a48c7976']
]
douai_safety = [
    ['Tokai1_Douai', 'Safety; Estop_OBI_IN_Detection_PCS; Safe PLC (Input)'],
    ['Tokai1_Douai', 'Safety; Estop_OBI_IN_DetectFeu_Batt2; Safe PLC (Input)'],
    ['Tokai1_Douai', 'Safety; Estop_OBI_IN_PB_Interne; Safe PLC (Input)'],
    ['Tokai1_Douai', 'Safety; Estop_OBI_IN_PB_PDL; Safe PLC (Input)']
]
douai_communication = [
    ['Tokai1_Douai', 'Communications; EC1_OBI_050Q1_Open; EC1 - The main auxiliary supply is open'],
    ['Tokai1_Douai', 'Communications; EC1_OBI_070Q2_Flt; EC1 - The 24 VDC supply of the TU is in fault'],
    ['Tokai1_Douai', 'Communications; TU_OBI_ComFlt; TU - At least one loss of comunication']
]
douai_battery = [
    ['Tokai1_Douai', 'Battery Fault; Rack']
]
douai_inverter = [
    ['Tokai1_Douai', 'Inverter Fault; With_OBI_UnexWithout; General - One Inverter has been unwilligly disconnected']
]
tokai1_douai = (
    douai_controller, 
    douai_safety,
    douai_communication,
    douai_battery,
    douai_inverter
)
douai_title = (f"\n" * 3 + "~" * 75 + " Tokai1_Douai (Douai) " + "~" * 75 + "\n")


# !!! `tokai 1 flins` alerts list with a title. Pass this two list into the main function
flins_controller = [
    ['fr_rte_tokai1_flins: is under required power Problem with the unitset described'],
    ['fr_rte_tokai1_flins_tu', 'FCR power 0 events over threshold!'],
    ['fr_rte_tokai1_flins_tu', 'has not changed frequency for 5min'],
    ['has lost connection', 'd46ffee5cb20a2193d8a0b17ff513bb0'],
    ['has lost connection', 'ad8ac6829b1d9c4b00869379985921f4'],
    ['has lost connection', '2bedfb43649d6f1e0fd1799b64c3158c'],
    ['has lost connection', 'e2635c6084e795aac5e06ea46e08b7b5'],
    ['has lost connection', '41ca718a3c5d2b3c57f3e0cbf4a0d360'],
    ['has lost connection', '4504be846bfad32e8b22ac4ba2db2f07'],
    ['has lost connection', '94f05cf07e78eb60f527120dffc9878b'],
    ['has lost connection', '3d9920c5aa673f2fd83826eda8ac4332'],
    ['has lost connection', '8cdc5fdf54a02b72cdc5997bed702e1c'],
    ['has lost connection', 'bcd809aa036371df9e2033433bcbdce1'],
    ['has lost connection', 'aa40f82bf5d8be228f10e5edba11210c'],
    ['has lost connection', '083ecaf064e7e64b0101cc0e2e4bf872'],
    ['has lost connection', 'e404ecd2563861b4e8853fe205691fae'],
    ['has lost connection', '0ff8ad0537eb61e964112d1fd598fda2'],
    ['has lost connection', '71d2e5dbd006b9bd0208bad327dcd712'],
    ['has lost connection', '294676f52954faf3de38e65e3ca9b321']
]
flins_safety = [
    ['fr_rte_tokai1_flins', 'Safety; Estop_OBI_IN_Detection_PCS; Safe PLC (Input)'],
    ['fr_rte_tokai1_flins', 'Safety; Estop_OBI_IN_DetectFeu_Batt2; Safe PLC (Input)'],
    ['fr_rte_tokai1_flins', 'Safety; Estop_OBI_IN_PB_Interne; Safe PLC (Input)'],
    ['fr_rte_tokai1_flins', 'Safety; Estop_OBI_IN_PB_PDL; Safe PLC (Input)']
]
flins_communication = [
    ['fr_rte_tokai1_flins', 'Communications; EC1_OBI_050Q1_Open; EC1 - The main auxiliary supply is open'],
    ['fr_rte_tokai1_flins', 'Communications; EC1_OBI_070Q2_Flt; EC1 - The 24 VDC supply of the TU is in fault'],
    ['fr_rte_tokai1_flins', 'Communications; TU_OBI_ComFlt; TU - At least one loss of comunication']
]
flins_battery = [
    ['fr_rte_tokai1_flins', 'Battery Fault; Rack']
]
flins_inverter = [
    ['fr_rte_tokai1_flins', 'Inverter Fault; With_OBI_UnexWithout; General - One Inverter has been unwilligly disconnected']
]
tokai1_flins = (
    flins_controller, 
    flins_safety,
    flins_communication,
    flins_battery,
    flins_inverter
)

flins_title = (f"\n" * 3 + "~" * 75 + " Tokai1_Flins (Flins) " + "~" * 75)


# !!! `tokai 2 elverlingsen` alerts list with a title. Pass this two list into the main function
tokai2_elverlingsen_alerts = [
    ['de_amp_tokai2', 'is under required power'],
    ['de_amp_tokai2', 'is under energy capacity'],
    ['Tokai2_Elverlingsen', 'FCR power 0 events over threshold!'],
    ['Tokai2_Elverlingsen', 'has not changed frequency for 5min'],
    ['Tokai2_Elverlingsen', 'ESS heartbeat errors above threshold!'], 
    ['has lost connection', 'd953641b710ce117c426744d61a45edc'],
    ['has lost connection', '3757f18d59a698e38535c7260937dee8'],
    ['has lost connection', '6d8d955d375109f29b576b3c68d5f6a9'],
    ['has lost connection', '583c9a3647ef8ddbcfc5c4af572f1e4c'],
    ['has lost connection', '7c58111584f4c4e397c17fe23c764130'],
    ['has lost connection', 'ff0ef17a6353899639cb31adcf700386'],
    ['has lost connection', 'fb28a334fb9b53e105a0c5f7bcb2d8cb'],
    ['has lost connection', '7df8ec6d0c876faed0789daeebbaa822']
]
tokai2_title = (f"\n" * 3 + "~" * 75 + " Tokai_2_Elverlingsen (ELV) " + "~" * 75)


# !!! `euref` alerts list with a title. Pass this two list into the main function
euref_storage = [
    ['“System Status” error or warning EUREF Storage']
]
euref_title = (f"\n" * 3 + "~" * 75 + " EURUF Storage " + "~" * 75)


# !!! `Prometheus` alerts list with a title. Pass this two list into the main function
prometheus = [
    ['Blackbox in mdex.bb.proc is down'],
    ['Blackbox in mdex.hs.proc is down'],
    ['Service prometheus prometheus_mdex.bb.proc is down'],
    ['Service prometheus prometheus_mdex.bb.tran is down'],
    ['Service prometheus prometheus_mdex.hs.proc is down'],
    ['Service prometheus prometheus_mdex.hs.tran is down'],
    ['Prometheus is not able to collect metrics about tmh-relay on instance proc101:8088 in mdex.hs.proc'],
    ['Server rabbit_3_7_1 in production.aggregator is under high load'],
    ['Host', 'monitored by Blackbox in production.aggregator is down'],
    ['RabbitMQ cluster in mdex.hs.tran has queue above threshold. Queue is logstash_events in vhost fluentd'],
    ['RabbitMQ cluster in mdex.bb.tran has queue above threshold. Queue is logstash_events in vhost fluentd'],
    ['Service nginx in production.aggregator is down'],
    ['Production Elastalert is down'],
    ['Host', 'monitored by Blackbox in production.aggregator is down'],
    ['RabbitMQ cluster in tmh.orange.arena has queue above threshold.'],
    ['Prometheus is not able to get information about rabbitmq cluster on instance rabbit_3_7_1 in production.aggregator'],
    ['Server storage of proc102 in mdex.hs.proc is almost full'],
    ['Server storage of proc002 in mdex.bb.proc will be full in 12 hours.'],
    ['Server storage in tmh.orange.arena will be full in 12 hours'],
    ['Storage in tmh.orange.arena is almost full. Usage is'],
    ['prometheus-bridge on proc002 in mdex.bb.proc is down'],
    ['Service prometheus prometheus_tmh.orange.arena is down'],
    ['Server storage of proc102 in mdex.hs.proc will be full in 12 hours'],
    ['Server storage of proc002 in mdex.bb.proc will be full in 12 hours.']
]
prometheus_title = (f"\n" * 3 + "~" * 75 + " Prometheus " + "~" * 75)


def process_alerts(alerts_list):
    """
    This function processes and counts specific alerts based on the provided list of alert groups. Takes a list of alert groups, 
    where each group is a list of keywords. It searches through the 'all_ack_alerts' list for each keyword in the group,
    and increments the counts of open and closed alerts accordingly.
    :param alerts_list: Tuple of lists, and alternatively a single list
    return: dict: A dictionary
    """
    for data in alerts_list:
        """
        Creating a dictionary where the keys are tuples of items from the list, 
        and the corresponding values are dictionaries with two keys: 'closed' and 'open
        """
        element_counts = {tuple(item): {'closed': 0, 'open': 0} for item in data}
        for entry in all_ack_alerts:                                # Iterate through each entry in the 'all_ack_alerts' list
            status = entry[1]
            for item in data:
                if all(keyword in entry[0] for keyword in item):    # Check if any keyword in the alert group matches the entry's name
                    element_counts[tuple(item)][status] += 1        # Push it to `element_counts`
    return element_counts

def print_alerts(alerts_counts):
    """
    Formats and prints the alert counts along with the title and totals.
    A dictionary containing alert groups and their respective open and closed counts.
    :param alerts_list: Tuple of lists, and alternatively a single list
    return: str: Formatted string
    """
    output = ""
    output += f"\n{'Alerts Name':<120} {'Open':<10} {'Closed':<10} {'Total':<10}\n"             # Print the title for the table
    output += '-' * 150 + "\n"
    for item, status_counts in alerts_counts.items():                                           # Iterate through each type of alert and its counts
        alert_name = item[0] if len(item) == 1 else ' '.join(item) + ' Alerts'                  # Generate the alert name based on the keywords in the item
        open_count = status_counts['open']                                                      # Find `open` alerts
        closed_count = status_counts['closed']                                                  # Find `closed` alerts
        total_count = open_count + closed_count                                                 # SUM both
        output += f"{alert_name:<120} {open_count:<10} {closed_count:<10} {total_count:<10}\n"  # Add the counts to the formating output (ex: Alert_Name - Open - Closed - Total)
    
    # Calculate the totals for each status
    open_alerts = sum(status_counts['open'] for status_counts in alerts_counts.values())
    closed_alerts = sum(status_counts['closed'] for status_counts in alerts_counts.values())
    total_alerts = sum(status_counts['closed'] + status_counts['open'] for status_counts in alerts_counts.values())

    # Add separators and the totals to the output
    output += '_' * 150 + "\n"
    output += f"{'Total Alerts':<120} {open_alerts:<10} {closed_alerts:<10} {total_alerts:<10}\n\n"
    
    return output

def main(alerts_list, title):
    """
    Process and print specific alerts counts from the given `alerts_list`.
    This function processes the lists, and pass that data to function for calculate alerts counts
    and then prints the formatted output along with subtotals and grand total.
    :param alerts_list: Tuple of lists, and alternatively a single list
    :param title: A string for the title
    :return: Formatted output
    """
    output = ""
    output += title + "\n"
    
    # If there is any `Tuple of lists`
    if isinstance(alerts_list, tuple):
        total_count = {}                                            # Initialize a dictionary to store the total counts
        for alerts_list in alerts_list:                             # Iterate through each alerts list in the tuple
            alerts_counts = process_alerts([alerts_list])           # Process the current alerts list and get the counts
            total_count.update(alerts_counts)                       # Update the total_count in the dictionary
            output += print_alerts(alerts_counts)                   # Formating the output with the counts for the current alerts list
            
        # Calculate the total & grand totals for each list
        open_alerts = sum(status_counts['open'] for status_counts in total_count.values())
        closed_alerts = sum(status_counts['closed'] for status_counts in total_count.values())
        grand_total = open_alerts + closed_alerts

        # Add separators and the grand totals to the output
        output += '=' * 170 + "\n"
        output += f"{'Grand Total Alerts':<120} {open_alerts:<10} {closed_alerts:<10} {grand_total:<10}\n\n"
    
    # Alternatively a single list
    else:
        alerts_counts = process_alerts([alerts_list])               # Process the current alerts list and get the counts
        output += print_alerts(alerts_counts)                       # Formating the output with the counts for the current alerts list
        
    print(output)

def top_10():
    """
    Get all controller alerts charging list through `All Ack Alerts List` and then find maximum number of alerts are generated.
    This code will display the controller alerts counts for each system,
    And the maximum number of alerts generated by the counter method.
    :return: None
    :print: descending order
    """
    print(f"\n" * 2 + "-" * 75 + " Top 10 Site ID & Count " + "-" * 75)
    # Filter all Charger UUID
    top_10 = []
    uuid = []
    # Find only controller alerts from `all_ack_alerts`
    for alert in all_ack_alerts:
        if 'Controller' in alert[0] and ('offline (last seen at' in alert[0] or 'chargers in error or offline' in alert[0]):
            top_10.append(alert[0])

    # Iterate through each item in the 'top_10' list
    for i in top_10:
        # Split the current item by spaces to separate words
        split_str = i.split(' ')
        # Get the second word and append it to the `uuid` list
        second_word = split_str[1]
        uuid.append(second_word)

    # Create a Counter object to count the items in the 'uuid' list
    counter = Counter(uuid)
    # Iterate through the top 10 most common items and their counts and print
    for item, count in counter.most_common(10):
        print(item, count)

def not_inCookbook():
    """
    This function identifies and prints the values from `All Ack Alerts List` that are not in Cookbook(included in the counts) based 
    on the conditions specified in `Combine List`(Charging, DE, AA, Tokai 1 & 2, Euref, Prometheus).
    :return: None
    :print: string
    """
    # Add all list in one combine list
    combined_list = charging_list + amsterdam_grid_alerts + de_alerts + fire_alarts + critical_storage + douai_controller + douai_safety + douai_communication + douai_battery + douai_inverter + flins_controller + flins_safety + flins_communication + flins_battery + flins_inverter + tokai2_elverlingsen_alerts + euref_storage + prometheus

    # Identify values from combined_list not included in the counts
    not_inCookbook_values = [entry for entry in all_ack_alerts if not any(all(keyword in entry[0] for keyword in item) for item in combined_list)]

    # If found minimum 1 alerts then print
    if(len(not_inCookbook_values) > 0):
        # Print the values from combined_list that are not included in the counts
        print(f"\n" * 3 + "~" * 70 + " Alerts are Ack'ed but not in Cookbook " + "~" * 70)
        print(f"Alerts are Ack'ed but not in Cookbook - counts: {len(not_inCookbook_values)}")
        for entry in not_inCookbook_values:
            print(entry)

def inCookbook_butNot_ack():
    """
    Cookbook alerts but unfortunately not acknowledged by Mulytic.
    This function identifies and prints the UnAcknowledgment alerts that are not included in the counts based
    on the conditions specified in `Combine List`(Charging, DE, AA, Tokai 1 & 2, Euref).
    :return: None
    :print: string
    """
    # Find out Un'Acked Alerts
    not_ack_alerts = []
    not_ack_count = 0
    # Iterate through each item from the `convert_to_list` list
    for alert in convert_to_list:
        # Checked Acknowledged False status & Owner of the alert by `support@mulytic.io` or `progga.roy@mulytic.io`
        if alert[2] == False and not (alert[4] == 'support@mulytic.io' or alert[4] == 'progga.roy@mulytic.io'):
            # Insert it to `unack_alerts` list
            not_ack_alerts.append(alert)
            not_ack_count = not_ack_count + 1

    # Add all list in one combine list
    combined_list = charging_list + amsterdam_grid_alerts + de_alerts + fire_alarts + critical_storage + douai_controller + douai_safety + douai_communication + douai_battery + douai_inverter + flins_controller + flins_safety + flins_communication + flins_battery + flins_inverter + tokai2_elverlingsen_alerts + euref_storage

    # Identify values from combined_list which are not not acknowledge by Mulytic from not_ack_alerts
    inCookbook_butNot_ack_values = [entry for entry in not_ack_alerts if any(all(keyword in entry[0] for keyword in item) for item in combined_list)]

    # If found minimum 1 alerts then print
    if(len(inCookbook_butNot_ack_values) > 0):
        # Print the values from combined_list that are not Acknowledged by Mulytic
        print(f"\n" * 3 + "~" * 70 + " Cookbook alerts but unfortunately not Ack'ed " + "~" * 70)
        print("Cookbook alerts but unfortunately not Ack'ed - Count:", len(inCookbook_butNot_ack_values))
        for entry in inCookbook_butNot_ack_values:
            print(entry)

def ack_byOthers():
    """
    This function identifies the values from `All Ack Alerts List` that are not acknowledged by Mulytic 
    based on the conditions specified in `Combine List`(Charging, DE, AA, Tokai 1 & 2, Euref, Prometheus).
    :return: None
    :print: string
    """
    ackBy_others = []
    ackBy_others_count = 0
    for alert in convert_to_list:
        # Checked Acknowledged True status & Not owner of the alert by `support@mulytic.io` or `progga.roy@mulytic.io`
        if alert[2] == True and not (alert[4] == 'support@mulytic.io' or alert[4] == 'progga.roy@mulytic.io'):
            # Insert it to `ackBy_others` list
            ackBy_others.append(alert)
            # print(ackBy_others)
            ackBy_others_count = ackBy_others_count + 1
    # Add all list in one combine list
    combined_list = charging_list + amsterdam_grid_alerts + de_alerts + fire_alarts + critical_storage + douai_controller + douai_safety + douai_communication + douai_battery + douai_inverter + flins_controller + flins_safety + flins_communication + flins_battery + flins_inverter + tokai2_elverlingsen_alerts + euref_storage + prometheus

    # Identify values from combined_list not included in the ackBy_others
    ackBy_others_values = [entry for entry in ackBy_others if any(all(keyword in entry[0] for keyword in item) for item in combined_list)]

    # If found minimum 1 alerts then print
    if(len(ackBy_others_values) > 0):
        # Print the values from combined_list that are not included in the ackBy_others
        print(f"\n" * 3 + "~" * 70 + " Alerts are Ack'ed by Others(Not Mulytic) " + "~" * 70)
        print(f"Alerts are Ack'ed by Others(Not Mulytic) - counts: {len(ackBy_others_values)}")
        for entry in ackBy_others_values:
            print(entry)

if __name__ == '__main__':
    """
    This block of code is executed when the script is run directly (not imported as a module).
    Calling function and passing its data like (Charging, DE, AA, Tokai 1 & 2, Euref, Prometheus).
    Calling the 'main' function with 2 parameters
    Also called `top_10` and `not_matched` function
    """
    main(charging_list, charging_title)
    main(german_grid, de_title)
    main(amsterdam_grid_alerts, aa_title)
    main(tokai1_douai, douai_title)
    main(tokai1_flins, flins_title)
    main(tokai2_elverlingsen_alerts, tokai2_title)
    main(euref_storage, euref_title)
    main(prometheus, prometheus_title)

    # Top 10 Sites ID Part Printing
    top_10()
    # Call this function to display alerts are not included in the counts
    not_inCookbook()
    # Call this function to display alerts are unfortunately not acknowledged by Mulytic
    inCookbook_butNot_ack()
    # Call this function to display alerts are acknowledged by Others
    ack_byOthers()

    # Close the redirected output file
    sys.stdout.close()

    # Restore sys.stdout to its original state
    sys.stdout = original_stdout

    # Print in console to take time in seconds to execute this script
    start = time.time()
    print(f'This script took {round(time.time() - start, 4)} seconds to generate the results')
