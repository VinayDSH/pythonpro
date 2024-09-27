import datetime

# Initialize lists to store tickets and agents
tickets = []
agents = {'Agent1': 'password1', 'Agent2': 'password2', 'Agent3': 'password3'}  # Agent: Password pairs
agent_index = 0  # This will help in assigning tickets to agents in round-robin fashion
current_agent = None  # To track the logged-in agent

# Function to create a ticket and automatically assign it to an agent
def create_ticket(ticket_id, issue, customer_name, priority):
    global agent_index
    
    if current_agent is None:
        print("You must be logged in to create a ticket.")
        return

    assigned_agent = list(agents.keys())[agent_index]  # Assign the current agent in round-robin order
    agent_index = (agent_index + 1) % len(agents)  # Move to the next agent
    
    ticket = {
        'id': ticket_id,
        'issue': issue,
        'customer_name': customer_name,
        'priority': priority,
        'created_at': datetime.datetime.now(),
        'assigned_to': assigned_agent,
        'status': 'Open',
        'resolution_time': None
    }
    tickets.append(ticket)
    print(f"Ticket {ticket_id} created and assigned to {assigned_agent}.")

# Function to resolve a ticket
def resolve_ticket(ticket_id):
    if current_agent is None:
        print("You must be logged in to resolve a ticket.")
        return

    for ticket in tickets:
        if ticket['id'] == ticket_id:
            if ticket['assigned_to'] != current_agent:
                print("You do not have permission to resolve this ticket.")
                return
            
            if ticket['status'] == 'Open':
                ticket['status'] = 'Resolved'
                ticket['resolution_time'] = datetime.datetime.now()
                print(f"Ticket {ticket_id} has been resolved.")
            else:
                print(f"Ticket {ticket_id} is already resolved.")
            return
    print(f"Ticket {ticket_id} not found.")

# Function to read tickets assigned to the logged-in agent
def read_tickets():
    if current_agent is None:
        print("You must be logged in to view tickets.")
        return
    
    agent_tickets = [ticket for ticket in tickets if ticket['assigned_to'] == current_agent]
    
    if not agent_tickets:
        print("No tickets assigned to you.")
        return

    for ticket in agent_tickets:
        print(f"Ticket ID: {ticket['id']}, Issue: {ticket['issue']}, Customer: {ticket['customer_name']}, "
              f"Priority: {ticket['priority']}, Status: {ticket['status']}, "
              f"Resolution Time: {ticket['resolution_time']}")

# Function to delete a ticket
def delete_ticket(ticket_id):
    global tickets
    
    if current_agent is None:
        print("You must be logged in to delete a ticket.")
        return
    
    # Check if the ticket belongs to the current agent
    tickets = [ticket for ticket in tickets if ticket['id'] != ticket_id or ticket['assigned_to'] != current_agent]
    print(f"Ticket {ticket_id} deleted.")

# Function to generate ticket resolution report
def generate_report():
    total_tickets = len(tickets)
    resolved_tickets = len([ticket for ticket in tickets if ticket['status'] == 'Resolved'])
    open_tickets = total_tickets - resolved_tickets
    
    print(f"Total Tickets: {total_tickets}")
    print(f"Resolved Tickets: {resolved_tickets}")
    print(f"Open Tickets: {open_tickets}")

# Function to log in an agent
def login_agent():
    global current_agent
    agent_name = input("Enter agent name: ")
    password = input("Enter password: ")
    
    if agent_name in agents and agents[agent_name] == password:
        current_agent = agent_name
        print(f"{agent_name} logged in successfully.")
    else:
        print("Invalid agent name or password.")

# Main execution loop
def main():
    global current_agent
    while True:
        if current_agent is None:
            print("\n--- Customer Support Ticketing System ---")
            print("1. Login as Agent")
            print("2. Exit")
            choice = input("Enter your choice (1-2): ")
            
            if choice == '1':
                login_agent()
            elif choice == '2':
                print("Exiting system.")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\n--- Customer Support Ticketing System ---")
            print("1. Create Ticket")
            print("2. Resolve Ticket")
            print("3. View My Tickets")
            print("4. Delete My Ticket")
            print("5. Generate Report")
            print("6. Logout")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                ticket_id = input("Enter ticket ID: ")
                issue = input("Enter issue: ")
                customer_name = input("Enter customer name: ")
                priority = input("Enter priority (High/Medium/Low): ")
                create_ticket(ticket_id, issue, customer_name, priority)
            elif choice == '2':
                ticket_id = input("Enter ticket ID: ")
                resolve_ticket(ticket_id)
            elif choice == '3':
                read_tickets()
            elif choice == '4':
                ticket_id = input("Enter ticket ID to delete: ")
                delete_ticket(ticket_id)
            elif choice == '5':
                generate_report()
            elif choice == '6':
                current_agent = None
                print("Logged out successfully.")
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
