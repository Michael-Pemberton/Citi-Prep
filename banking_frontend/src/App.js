import React from 'react';
import { BrowserRouter, Routes, Route, NavLink, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Accounts from './pages/Accounts';

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="nav-section">
        <div className="nav-label">Overview</div>
        <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
          <span className="nav-icon">◈</span> Dashboard
        </NavLink>
      </div>
      <div className="nav-section">
        <div className="nav-label">Management</div>
        <NavLink to="/customers" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
          <span className="nav-icon">◉</span> Customers
        </NavLink>
        <NavLink to="/accounts" className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
          <span className="nav-icon">◈</span> Accounts
        </NavLink>
      </div>
    </aside>
  );
}

function Layout({ children }) {
  return (
    <div className="layout">
      <header className="topbar">
        <div className="topbar-logo">
          Michael <span>Banking Platform</span>
        </div>
        <div className="topbar-status">
          <div className="status-dot" />
          API Connected
        </div>
      </header>
      <Sidebar />
      <main className="main-content">{children}</main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/accounts" element={<Accounts />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
