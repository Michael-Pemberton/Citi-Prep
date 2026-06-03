import React, { useEffect, useState } from 'react';
import { getCustomers, getAccounts } from '../api';
import { Link } from 'react-router-dom';

function fmt(n) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);
}

export default function Dashboard() {
  const [customers, setCustomers] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getCustomers(), getAccounts()])
      .then(([c, a]) => {
        setCustomers(c.data);
        setAccounts(a.data);
      })
      .finally(() => setLoading(false));
  }, []);

  const totalBalance = accounts.reduce((s, a) => s + parseFloat(a.balance || 0), 0);
  const savings = accounts.filter(a => a.account_type === 'Savings');
  const checking = accounts.filter(a => a.account_type === 'Checking');
  const savingsTotal = savings.reduce((s, a) => s + parseFloat(a.balance || 0), 0);
  const checkingTotal = checking.reduce((s, a) => s + parseFloat(a.balance || 0), 0);

  // Top 5 customers by balance
  const customerBalances = customers.map(c => ({
    ...c,
    total: accounts.filter(a => a.customer_id === c.id).reduce((s, a) => s + parseFloat(a.balance || 0), 0),
  })).sort((a, b) => b.total - a.total).slice(0, 5);

  if (loading) return (
    <div className="loading"><div className="spinner" /> Loading dashboard…</div>
  );

  return (
    <>
      <div className="page-header">
        <div className="page-title">
          Dashboard
          <span>Real-time overview of your banking platform</span>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Customers</div>
          <div className="stat-value gold">{customers.length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total Accounts</div>
          <div className="stat-value">{accounts.length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total AUM</div>
          <div className="stat-value gold" style={{ fontSize: 24 }}>{fmt(totalBalance)}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Savings Balance</div>
          <div className="stat-value green" style={{ fontSize: 22 }}>{fmt(savingsTotal)}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Checking Balance</div>
          <div className="stat-value" style={{ fontSize: 22 }}>{fmt(checkingTotal)}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Avg Balance / Account</div>
          <div className="stat-value" style={{ fontSize: 22 }}>
            {accounts.length ? fmt(totalBalance / accounts.length) : '$0'}
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="card">
          <div className="card-header">
            <span className="card-title">Top Customers by Balance</span>
            <Link to="/customers" className="btn btn-ghost btn-sm">View all</Link>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Customer</th>
                  <th>Email</th>
                  <th>Total Balance</th>
                </tr>
              </thead>
              <tbody>
                {customerBalances.length === 0 && (
                  <tr><td colSpan={3}><div className="empty"><div className="empty-text">No customers yet</div></div></td></tr>
                )}
                {customerBalances.map(c => (
                  <tr key={c.id}>
                    <td style={{ fontWeight: 500 }}>{c.name}</td>
                    <td style={{ color: 'var(--text-dim)' }}>{c.email}</td>
                    <td><span className="amount">{fmt(c.total)}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <span className="card-title">Recent Accounts</span>
            <Link to="/accounts" className="btn btn-ghost btn-sm">View all</Link>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Number</th>
                  <th>Type</th>
                  <th>Balance</th>
                </tr>
              </thead>
              <tbody>
                {accounts.length === 0 && (
                  <tr><td colSpan={3}><div className="empty"><div className="empty-text">No accounts yet</div></div></td></tr>
                )}
                {accounts.slice(-5).reverse().map(a => (
                  <tr key={a.id}>
                    <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{a.account_number}</td>
                    <td>
                      <span className={`badge badge-${a.account_type?.toLowerCase()}`}>
                        {a.account_type}
                      </span>
                    </td>
                    <td><span className="amount">{fmt(a.balance)}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}
