#include <iostream>
#include <vector>
#include <memory>
#include <string>
#include <iomanip>
#include <stdexcept>

using namespace std;


class ITransaction
{
public:
    virtual void PrintReceipt() = 0;
    virtual ~ITransaction() {}
};

class Account;


class Customer
{
private:
    int customerID;
    string firstName;
    string lastName;

public:
    vector<shared_ptr<Account>> accounts;

    Customer(int id, string first, string last)
        : customerID(id), firstName(first), lastName(last) {}

    int GetCustomerID() const { return customerID; }
    string GetFirstName() const { return firstName; }
    string GetLastName() const { return lastName; }
};


class Account : public ITransaction
{
protected:
    string accountNumber;
    Customer* accountHolder;
    double balance;

public:
    Account(string accNum, Customer* holder, double bal)
        : accountNumber(accNum), accountHolder(holder), balance(bal) {}

    virtual ~Account() {}

    virtual void Deposit(double amount)
    {
        if (amount <= 0)
            throw invalid_argument("Deposit must be positive.");

        balance += amount;
    }

    virtual bool Withdraw(double amount) = 0;

    virtual string GetType() const = 0;

    double GetBalance() const { return balance; }
    string GetAccountNumber() const { return accountNumber; }
    Customer* GetCustomer() const { return accountHolder; }

    virtual void PrintReceipt() override
    {
        cout << "\n========== RECEIPT ==========\n";
        cout << "Account: " << accountNumber << endl;
        cout << "Balance: $" << fixed << setprecision(2)
             << balance << endl;
        cout << "=============================\n";
    }
};


class SavingsAccount : public Account
{
private:
    double interestRate;

public:
    SavingsAccount(string accNum,
                   Customer* holder,
                   double bal,
                   double rate)
        : Account(accNum, holder, bal),
          interestRate(rate) {}

    bool Withdraw(double amount) override
    {
        if (amount <= 0)
            throw invalid_argument("Amount must be positive.");

        if ((balance - amount) < 100)
        {
            cout << "Savings account must maintain $100 minimum balance.\n";
            return false;
        }

        balance -= amount;
        return true;
    }

    string GetType() const override
    {
        return "Savings";
    }
};


class CheckingAccount : public Account
{
private:
    double overdraftLimit;

public:
    CheckingAccount(string accNum,
                    Customer* holder,
                    double bal,
                    double limit)
        : Account(accNum, holder, bal),
          overdraftLimit(limit) {}

    bool Withdraw(double amount) override
    {
        if (amount <= 0)
            throw invalid_argument("Amount must be positive.");

        if ((balance - amount) < -overdraftLimit)
        {
            cout << "Overdraft limit exceeded.\n";
            return false;
        }

        balance -= amount;
        return true;
    }

    string GetType() const override
    {
        return "Checking";
    }
};


vector<Customer> customers;


shared_ptr<Account> FindAccount(string accNum)
{
    for (auto& customer : customers)
    {
        for (auto& account : customer.accounts)
        {
            if (account->GetAccountNumber() == accNum)
                return account;
        }
    }

    return nullptr;
}


void SeedData()
{
    Customer c1(1, "John", "Smith");
    Customer c2(2, "Jane", "Doe");

    c1.accounts.push_back(
        make_shared<SavingsAccount>(
            "S1001",
            &c1,
            1000,
            0.03));

    c1.accounts.push_back(
        make_shared<CheckingAccount>(
            "C1001",
            &c1,
            500,
            300));

    c2.accounts.push_back(
        make_shared<SavingsAccount>(
            "S2001",
            &c2,
            2000,
            0.04));

    customers.push_back(c1);
    customers.push_back(c2);
}


void CreateAccount()
{
    int id;
    string first, last;
    string accNum;
    int type;

    cout << "Customer ID: ";
    cin >> id;

    cout << "First Name: ";
    cin >> first;

    cout << "Last Name: ";
    cin >> last;

    Customer customer(id, first, last);

    cout << "\n1. Savings\n";
    cout << "2. Checking\n";
    cout << "Choice: ";
    cin >> type;

    cout << "Account Number: ";
    cin >> accNum;

    if (type == 1)
    {
        customer.accounts.push_back(
            make_shared<SavingsAccount>(
                accNum,
                &customer,
                500,
                0.03));
    }
    else
    {
        customer.accounts.push_back(
            make_shared<CheckingAccount>(
                accNum,
                &customer,
                500,
                300));
    }

    customers.push_back(customer);

    cout << "Account created successfully.\n";
}


void ViewAccounts()
{
    cout << "\n===== ACCOUNTS =====\n";

    for (auto& customer : customers)
    {
        for (auto& account : customer.accounts)
        {
            cout << account->GetType()
                 << " | "
                 << account->GetAccountNumber()
                 << " | "
                 << customer.GetFirstName()
                 << " "
                 << customer.GetLastName()
                 << " | Balance: $"
                 << fixed << setprecision(2)
                 << account->GetBalance()
                 << endl;
        }
    }
}


void Deposit()
{
    string accNum;
    double amount;

    cout << "Account Number: ";
    cin >> accNum;

    auto account = FindAccount(accNum);

    if (!account)
    {
        cout << "Account not found.\n";
        return;
    }

    cout << "Amount: ";
    cin >> amount;

    account->Deposit(amount);
    account->PrintReceipt();
}



void Withdraw()
{
    string accNum;
    double amount;

    cout << "Account Number: ";
    cin >> accNum;

    auto account = FindAccount(accNum);

    if (!account)
    {
        cout << "Account not found.\n";
        return;
    }

    cout << "Amount: ";
    cin >> amount;

    if (account->Withdraw(amount))
    {
        account->PrintReceipt();
    }
}


void Transfer()
{
    string source;
    string destination;
    double amount;

    cout << "Source Account: ";
    cin >> source;

    cout << "Destination Account: ";
    cin >> destination;

    cout << "Amount: ";
    cin >> amount;

    auto from = FindAccount(source);
    auto to = FindAccount(destination);

    if (!from || !to)
    {
        cout << "Invalid account number.\n";
        return;
    }

    if (from->Withdraw(amount))
    {
        to->Deposit(amount);

        cout << "Transfer successful.\n";
        from->PrintReceipt();
        to->PrintReceipt();
    }
}


void CloseAccount()
{
    string accNum;

    cout << "Account Number: ";
    cin >> accNum;

    for (auto& customer : customers)
    {
        auto& accounts = customer.accounts;

        for (auto it = accounts.begin();
             it != accounts.end();
             ++it)
        {
            if ((*it)->GetAccountNumber() == accNum)
            {
                accounts.erase(it);
                cout << "Account closed.\n";
                return;
            }
        }
    }

    cout << "Account not found.\n";
}


int main()
{
    SeedData();

    int choice;

    while (true)
    {
        try
        {
            cout << "\n===== BANK =====\n";
            cout << "1. Create Account\n";
            cout << "2. View Accounts\n";
            cout << "3. Deposit\n";
            cout << "4. Withdraw\n";
            cout << "5. Transfer\n";
            cout << "6. Close Account\n";
            cout << "7. Exit\n";
            cout << "Choice: ";

            cin >> choice;

            switch (choice)
            {
            case 1:
                CreateAccount();
                break;

            case 2:
                ViewAccounts();
                break;

            case 3:
                Deposit();
                break;

            case 4:
                Withdraw();
                break;

            case 5:
                Transfer();
                break;

            case 6:
                CloseAccount();
                break;

            case 7:
                return 0;

            default:
                cout << "Invalid choice.\n";
            }
        }
        catch (exception& ex)
        {
            cout << "Error" <<  endl;
        }
    }

    return 0;
}
