import React, { useEffect, useState } from 'react';
import {
  getCustomers, createCustomer, updateCustomer, deleteCustomer
} from '../api';
import ConfirmDialog from '../components/ConfirmDialog';

function fmt(n) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);
}

function CustomerModal({ customer, onClose, onSave }) {
  const [form, setForm] = useState({ name: customer?.name || '', email: customer?.email || '' });
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const isEdit = !!customer;

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  async function submit(e) {
    e.preventDefault();
    if (!form.name.trim() || !form.email.trim()) { setError('Name and email are required.'); return; }
    setSaving(true);
    try {
      if (isEdit) {
        await updateCustomer(customer.id, form);
      } else {
        await createCustomer(form);
      }
      onSave();
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong.');
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-title">{isEdit ? 'Edit Customer' : 'New Customer'}</div>
        {error && <div className="alert alert-error">{error}</div>}
        <form onSubmit={submit}>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input className="form-input" placeholder="Jane Smith" value={form.name}
              onChange={e => set('name', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input className="form-input" type="email" placeholder="jane@example.com" value={form.email}
              onChange={e => set('email', e.target.value)} />
          </div>
          <div className="modal-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving…' : isEdit ? 'Save Changes' : 'Create Customer'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [modal, setModal] = useState(null); // null | 'create' | { customer }
  const [confirm, setConfirm] = useState(null); // null | { id, name }
  const [expanded, setExpanded] = useState(null);

  const load = () => {
    setLoading(true);
    getCustomers().then(r => setCustomers(r.data)).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const filtered = customers.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.email.toLowerCase().includes(search.toLowerCase())
  );

  async function handleDelete(id) {
    await deleteCustomer(id);
    setConfirm(null);
    load();
  }

  function toggleExpand(id) {
    setExpanded(prev => prev === id ? null : id);
  }

  return (
    <>
      {modal === 'create' && (
        <CustomerModal onClose={() => setModal(null)} onSave={() => { setModal(null); load(); }} />
      )}
      {modal?.customer && (
        <CustomerModal customer={modal.customer} onClose={() => setModal(null)} onSave={() => { setModal(null); load(); }} />
      )}
      {confirm && (
        <ConfirmDialog
          title="Delete Customer"
          message="You are about to permanently delete"
          name={confirm.name}
          onConfirm={() => handleDelete(confirm.id)}
          onCancel={() => setConfirm(null)}
        />
      )}

      <div className="page-header">
        <div className="page-title">
          Customers
          <span>{customers.length} total customers</span>
        </div>
        <button className="btn btn-primary" onClick={() => setModal('create')}>
          + New Customer
        </button>
      </div>

      <div className="card">
        <div className="card-header">
          <span className="card-title">All Customers</span>
          <div className="search-bar">
            <span style={{ color: 'var(--text-muted)' }}>⌕</span>
            <input placeholder="Search by name or email…" value={search}
              onChange={e => setSearch(e.target.value)} />
          </div>
        </div>

        {loading ? (
          <div className="loading"><div className="spinner" /> Loading…</div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Accounts</th>
                  <th>Total Balance</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={6}>
                      <div className="empty">
                        <div className="empty-icon">◎</div>
                        <div className="empty-text">No customers found</div>
                      </div>
                    </td>
                  </tr>
                )}
                {filtered.map(c => {
                  const total = (c.accounts || []).reduce((s, a) => s + parseFloat(a.balance || 0), 0);
                  const isOpen = expanded === c.id;
                  return (
                    <React.Fragment key={c.id}>
                      <tr>
                        <td style={{ color: 'var(--text-muted)', fontSize: 12 }}>#{c.id}</td>
                        <td style={{ fontWeight: 500 }}>{c.name}</td>
                        <td style={{ color: 'var(--text-dim)' }}>{c.email}</td>
                        <td>
                          <button
                            className="btn btn-ghost btn-sm"
                            onClick={() => toggleExpand(c.id)}
                          >
                            {c.accounts?.length || 0} {isOpen ? '▲' : '▼'}
                          </button>
                        </td>
                        <td><span className="amount">{fmt(total)}</span></td>
                        <td>
                          <div className="actions-cell">
                            <button className="btn btn-edit"
                              onClick={() => setModal({ customer: c })}>
                              Edit
                            </button>
                            <button className="btn btn-danger"
                              onClick={() => setConfirm({ id: c.id, name: c.name })}>
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                      {isOpen && (
                        <tr className="expand-row">
                          <td colSpan={6}>
                            <div className="expand-inner">
                              {(!c.accounts || c.accounts.length === 0) ? (
                                <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>No accounts linked to this customer.</span>
                              ) : (
                                <div className="accounts-mini-table">
                                  <table>
                                    <thead>
                                      <tr>
                                        <th>Account #</th>
                                        <th>Type</th>
                                        <th>Balance</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      {c.accounts.map(a => (
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
                              )}
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
