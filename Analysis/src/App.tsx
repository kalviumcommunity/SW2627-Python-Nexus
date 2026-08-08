import { useState, useMemo } from 'react';
import { BLOCKER_DATA } from './data/blockerData';
import type { Blocker } from './data/blockerData';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, CartesianGrid
} from 'recharts';
import {
  AlertTriangle, CheckCircle2, Clock, Layers, Users,
  Filter, RefreshCw, Download, Search, ShieldAlert, TrendingUp
} from 'lucide-react';

const COLOR_PALETTE = {
  primary: '#1E88E5',
  success: '#10B981',
  warning: '#F59E0B',
  critical: '#EF4444',
  neutral: '#6B7280',
  indigo: '#6366F1',
  teal: '#14B8A6'
};

export default function App() {
  // Filter States
  const allTeams = useMemo(() => Array.from(new Set(BLOCKER_DATA.map(d => d.team_id))).sort(), []);
  const allSprints = useMemo(() => Array.from(new Set(BLOCKER_DATA.map(d => d.sprint_id))).sort(), []);
  const allCategories = useMemo(() => Array.from(new Set(BLOCKER_DATA.map(d => d.category))).sort(), []);
  const allStatuses = useMemo(() => Array.from(new Set(BLOCKER_DATA.map(d => d.status))).sort(), []);

  const [selectedTeams, setSelectedTeams] = useState<string[]>(allTeams);
  const [selectedSprints, setSelectedSprints] = useState<string[]>(allSprints);
  const [selectedCategories, setSelectedCategories] = useState<string[]>(allCategories);
  const [selectedStatuses, setSelectedStatuses] = useState<string[]>(allStatuses);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'overview' | 'trends' | 'rootcause' | 'explorer'>('overview');

  // Multi-select Helper
  const toggleSelection = (list: string[], setList: (l: string[]) => void, item: string) => {
    if (list.includes(item)) {
      if (list.length > 1) setList(list.filter(i => i !== item));
    } else {
      setList([...list, item]);
    }
  };

  const resetFilters = () => {
    setSelectedTeams(allTeams);
    setSelectedSprints(allSprints);
    setSelectedCategories(allCategories);
    setSelectedStatuses(allStatuses);
    setSearchTerm('');
  };

  // Filtered Dataset Computation
  const filteredData = useMemo(() => {
    return BLOCKER_DATA.filter((item: Blocker) => {
      const matchTeam = selectedTeams.includes(item.team_id);
      const matchSprint = selectedSprints.includes(item.sprint_id);
      const matchCategory = selectedCategories.includes(item.category);
      const matchStatus = selectedStatuses.includes(item.status);
      const matchSearch = searchTerm === '' ||
        item.blocker_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.category.toLowerCase().includes(searchTerm.toLowerCase());
      return matchTeam && matchSprint && matchCategory && matchStatus && matchSearch;
    });
  }, [selectedTeams, selectedSprints, selectedCategories, selectedStatuses, searchTerm]);

// =====================================================
// KPI CALCULATIONS
// =====================================================

const kpis = useMemo(() => {
  const total = filteredData.length;

  if (total === 0) {
    return {
      total: 0,
      resolved: 0,
      rate: '0%',
      avgResolution: '0d',
      externalPct: '0%',
      topTeam: 'N/A',
      topTeamCount: 0,
      topCategory: 'N/A',
      topCategoryCount: 0
    };
  }

  // Resolved blockers
  const resolved = filteredData.filter(
    d => d.status.toLowerCase() === 'resolved'
  ).length;

  const rate = ((resolved / total) * 100).toFixed(1) + '%';

  // Average resolution time
  const avgResolutionValue =
    filteredData.reduce(
      (sum, d) => sum + d.resolution_time_days,
      0
    ) / total;

  const avgResolution =
    avgResolutionValue.toFixed(1) + 'd';

  // External dependencies
  const externalCount = filteredData.filter(
    d => d.is_external_dependency
  ).length;

  const externalPct =
    ((externalCount / total) * 100).toFixed(1) + '%';

  // -----------------------------------------
  // Top Team
  // -----------------------------------------

  const teamCounts: Record<string, number> = {};

  filteredData.forEach(d => {
    teamCounts[d.team_id] =
      (teamCounts[d.team_id] || 0) + 1;
  });

  const sortedTeams = Object.entries(teamCounts)
    .sort((a, b) => b[1] - a[1]);

  const topTeam =
    sortedTeams[0]?.[0] || 'N/A';

  const topTeamCount =
    sortedTeams[0]?.[1] || 0;

  // -----------------------------------------
  // Top Category
  // -----------------------------------------

  const categoryCounts: Record<string, number> = {};

  filteredData.forEach(d => {
    categoryCounts[d.category] =
      (categoryCounts[d.category] || 0) + 1;
  });

  const sortedCategories = Object.entries(categoryCounts)
    .sort((a, b) => b[1] - a[1]);

  const topCategory =
    sortedCategories[0]?.[0] || 'N/A';

  const topCategoryCount =
    sortedCategories[0]?.[1] || 0;

  return {
    total,
    resolved,
    rate,
    avgResolution,
    externalPct,
    topTeam,
    topTeamCount,
    topCategory,
    topCategoryCount
  };

}, [filteredData]);


// =====================================================
// BUSINESS INSIGHTS
// =====================================================

const businessInsights = useMemo(() => {

  if (filteredData.length === 0) {
    return {
      externalImpact: 'No data available.',
      teamRisk: 'No data available.',
      categoryRisk: 'No data available.'
    };
  }

  const externalCount = filteredData.filter(
    d => d.is_external_dependency
  ).length;

  const externalPercentage =
    (externalCount / filteredData.length) * 100;

  let externalImpact = '';

  if (externalPercentage >= 40) {
    externalImpact =
      `External dependencies are a major delivery risk, affecting ${externalPercentage.toFixed(1)}% of blockers.`;
  } else if (externalPercentage >= 20) {
    externalImpact =
      `External dependencies have a moderate impact, affecting ${externalPercentage.toFixed(1)}% of blockers.`;
  } else {
    externalImpact =
      `External dependencies have relatively low impact at ${externalPercentage.toFixed(1)}% of blockers.`;
  }

  const teamRisk =
    `${kpis.topTeam} has the highest blocker volume with ${kpis.topTeamCount} recorded issues.`;

  const categoryRisk =
    `${kpis.topCategory} is the most frequent blocker category with ${kpis.topCategoryCount} incidents.`;

  return {
    externalImpact,
    teamRisk,
    categoryRisk
  };

}, [filteredData, kpis]);


// =====================================================
// CATEGORY RESOLUTION ANALYSIS
// =====================================================

const categoryResolution = useMemo(() => {

  if (filteredData.length === 0) {
    return {
      category: 'N/A',
      avgDays: 0
    };
  }

  const categoryStats: Record<
    string,
    {
      totalDays: number;
      count: number;
    }
  > = {};

  filteredData.forEach(d => {

    if (!categoryStats[d.category]) {
      categoryStats[d.category] = {
        totalDays: 0,
        count: 0
      };
    }

    categoryStats[d.category].totalDays +=
      d.resolution_time_days;

    categoryStats[d.category].count += 1;
  });

  const highestCategory = Object.entries(categoryStats)
    .map(([category, stats]) => ({
      category,
      avgDays: stats.totalDays / stats.count
    }))
    .sort((a, b) => b.avgDays - a.avgDays)[0];

  return {
    category: highestCategory?.category || 'N/A',
    avgDays: highestCategory?.avgDays || 0
  };

}, [filteredData]);


// =====================================================
// CHART DATA
// =====================================================

const categoryChartData = useMemo(() => {

  const counts: Record<string, number> = {};

  filteredData.forEach(d => {
    counts[d.category] =
      (counts[d.category] || 0) + 1;
  });

  return Object.entries(counts)
    .map(([name, count]) => ({
      name,
      count
    }))
    .sort((a, b) => b.count - a.count);

}, [filteredData]);


const teamChartData = useMemo(() => {

  const counts: Record<string, number> = {};

  filteredData.forEach(d => {
    counts[d.team_id] =
      (counts[d.team_id] || 0) + 1;
  });

  return Object.entries(counts)
    .map(([name, count]) => ({
      name,
      count
    }))
    .sort((a, b) => a.count - b.count);

}, [filteredData]);


const dependencyChartData = useMemo(() => {

  const external =
    filteredData.filter(
      d => d.is_external_dependency
    ).length;

  const internal =
    filteredData.length - external;

  return [
    {
      name: 'External Dependency',
      value: external,
      color: COLOR_PALETTE.warning
    },
    {
      name: 'Internal Coordination',
      value: internal,
      color: COLOR_PALETTE.primary
    }
  ];

}, [filteredData]);


const trendChartData = useMemo(() => {

  const dates: Record<string, number> = {};

  filteredData.forEach(d => {
    dates[d.date_logged] =
      (dates[d.date_logged] || 0) + 1;
  });

  return Object.entries(dates)
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([date, count]) => ({
      date: date.slice(5),
      count
    }));

}, [filteredData]);


const sprintCategoryHeatmapData = useMemo(() => {

  const matrix: Record<
    string,
    Record<string, number>
  > = {};

  filteredData.forEach(d => {

    if (!matrix[d.sprint_id]) {
      matrix[d.sprint_id] = {};
    }

    matrix[d.sprint_id][d.category] =
      (matrix[d.sprint_id][d.category] || 0) + 1;
  });

  return Object.entries(matrix)
    .map(([sprint, categories]) => ({
      sprint,
      ...categories
    }))
    .sort((a, b) =>
      a.sprint.localeCompare(b.sprint)
    );

}, [filteredData]);

  // Download CSV helper
  const exportCSV = () => {
    const headers = ['blocker_id', 'team_id', 'sprint_id', 'date_logged', 'category', 'is_external_dependency', 'resolution_time_days', 'status', 'description'];
    const rows = filteredData.map(d => [
      d.blocker_id, d.team_id, d.sprint_id, d.date_logged, `"${d.category}"`, d.is_external_dependency, d.resolution_time_days, d.status, `"${d.description}"`
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `blocker_analytics_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-800 antialiased overflow-hidden">

      {/* SIDEBAR FILTERS */}
      <aside className="w-80 bg-white border-r border-slate-200 p-5 flex flex-col justify-between overflow-y-auto shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-6 pb-4 border-b border-slate-100">
            <Filter className="w-5 h-5 text-blue-600" />
            <h2 className="font-bold text-lg text-slate-900">Interactive Filters</h2>
          </div>

          {/* Teams Filter */}
          <div className="mb-6">
            <label className="text-xs font-semibold uppercase text-slate-500 tracking-wider mb-2 block">Engineering Team</label>
            <div className="flex flex-wrap gap-1.5">
              {allTeams.map(team => {
                const active = selectedTeams.includes(team);
                return (
                  <button
                    key={team}
                    onClick={() => toggleSelection(selectedTeams, setSelectedTeams, team)}
                    className={`text-xs px-2.5 py-1 rounded-md font-medium transition-all ${active ? 'bg-blue-600 text-white shadow-xs' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                  >
                    {team}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Sprints Filter */}
          <div className="mb-6">
            <label className="text-xs font-semibold uppercase text-slate-500 tracking-wider mb-2 block">Sprint Cycle</label>
            <div className="flex flex-wrap gap-1.5">
              {allSprints.map(sprint => {
                const active = selectedSprints.includes(sprint);
                return (
                  <button
                    key={sprint}
                    onClick={() => toggleSelection(selectedSprints, setSelectedSprints, sprint)}
                    className={`text-xs px-2.5 py-1 rounded-md font-medium transition-all ${active ? 'bg-blue-600 text-white shadow-xs' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                  >
                    {sprint}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Categories Filter */}
          <div className="mb-6">
            <label className="text-xs font-semibold uppercase text-slate-500 tracking-wider mb-2 block">Blocker Category</label>
            <div className="flex flex-col gap-1.5">
              {allCategories.map(cat => {
                const active = selectedCategories.includes(cat);
                return (
                  <button
                    key={cat}
                    onClick={() => toggleSelection(selectedCategories, setSelectedCategories, cat)}
                    className={`text-xs px-3 py-1.5 rounded-md font-medium text-left flex items-center justify-between transition-all ${active ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-slate-50 text-slate-600 hover:bg-slate-100'
                      }`}
                  >
                    <span>{cat}</span>
                    {active && <CheckCircle2 className="w-3.5 h-3.5 text-blue-600" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Status Filter */}
          <div className="mb-6">
            <label className="text-xs font-semibold uppercase text-slate-500 tracking-wider mb-2 block">Ticket Status</label>
            <div className="flex gap-2">
              {allStatuses.map(status => {
                const active = selectedStatuses.includes(status);
                return (
                  <button
                    key={status}
                    onClick={() => toggleSelection(selectedStatuses, setSelectedStatuses, status)}
                    className={`text-xs px-3 py-1.5 rounded-md font-medium transition-all ${active ? 'bg-emerald-600 text-white shadow-xs' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                  >
                    {status}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        <button
          onClick={resetFilters}
          className="w-full flex items-center justify-center gap-2 py-2 px-4 border border-slate-200 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Reset All Filters
        </button>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col overflow-hidden">

        {/* TOP EXECUTIVE HEADER */}
        <header className="bg-gradient-to-r from-blue-700 to-indigo-900 text-white p-6 shadow-md">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Remote Engineering Delivery Intelligence Dashboard</h1>
              <p className="text-blue-100 text-sm mt-1">Leadership Analytics for Identifying Systemic Delivery Bottlenecks & Recurring Blockers</p>
            </div>
          </div>
        </header>

        {/* DYNAMIC KPI CARDS SECTION */}
        <section className="bg-white border-b border-slate-200 p-5 shadow-xs">
          <div className="max-w-7xl mx-auto grid grid-cols-7 gap-4">

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Total Blockers</p>
              <p className="text-xl font-bold text-slate-900 mt-1">{kpis.total}</p>
              <p className="text-[11px] text-slate-500 mt-0.5">Logged Issues</p>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Resolved</p>
              <p className="text-xl font-bold text-slate-900 mt-1">{kpis.resolved}</p>
              <p className="text-[11px] text-slate-500 mt-0.5">Closed Tickets</p>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Resolution Rate</p>
              <p className="text-xl font-bold text-emerald-600 mt-1">{kpis.rate}</p>
              <p className="text-[11px] text-slate-500 mt-0.5">Completion Ratio</p>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Avg Resolution</p>
              <p className="text-xl font-bold text-slate-900 mt-1">{kpis.avgResolution}</p>
              <p className="text-[11px] text-slate-500 mt-0.5">Days to Close</p>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">External Dep.</p>
              <p className="text-xl font-bold text-amber-600 mt-1">{kpis.externalPct}</p>
              <p className="text-[11px] text-slate-500 mt-0.5">3rd Party Dependency</p>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Top Team</p>
              <p className="text-sm font-bold text-slate-900 mt-1 truncate">{kpis.topTeam}</p>
              <p className="text-[11px] text-slate-500 mt-0.5">{kpis.topTeamCount} Blockers</p>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Top Category</p>
              <p className="text-xs font-bold text-slate-900 mt-1 truncate">{kpis.topCategory}</p>
              <p className="text-[11px] text-slate-500 mt-0.5">{kpis.topCategoryCount} Incidents</p>
            </div>

          </div>
        </section>
                {/* BUSINESS HEALTH / ALERTS */}

        <section className="bg-slate-50 border-b border-slate-200 px-5 py-4">
          <div className="max-w-7xl mx-auto">

            <div className="flex items-center justify-between mb-3">
              <div>
                <h2 className="text-sm font-bold text-slate-900">
                  Business Health
                </h2>
                <p className="text-xs text-slate-500">
                  Automated signals based on the currently selected filters
                </p>
              </div>

              <div className="flex items-center gap-2 text-xs text-slate-500">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                Live analysis
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">

              {/* Resolution Health */}
              <div className="bg-white border border-slate-200 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500">
                    Resolution Health
                  </span>

                  <span
                    className={`text-xs font-bold px-2 py-1 rounded-full ${
                      parseFloat(kpis.avgResolution) > 3
                        ? 'bg-amber-100 text-amber-700'
                        : 'bg-emerald-100 text-emerald-700'
                    }`}
                  >
                    {parseFloat(kpis.avgResolution) > 3
                      ? 'Attention'
                      : 'Healthy'}
                  </span>
                </div>

                <p className="text-lg font-bold text-slate-900 mt-2">
                  {kpis.avgResolution}
                </p>

                <p className="text-xs text-slate-500">
                  Average blocker resolution time
                </p>
              </div>

              {/* Dependency Health */}
              <div className="bg-white border border-slate-200 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500">
                    Dependency Risk
                  </span>

                  <span
                    className={`text-xs font-bold px-2 py-1 rounded-full ${
                      parseFloat(kpis.externalPct) >= 30
                        ? 'bg-red-100 text-red-700'
                        : 'bg-emerald-100 text-emerald-700'
                    }`}
                  >
                    {parseFloat(kpis.externalPct) >= 30
                      ? 'High Risk'
                      : 'Controlled'}
                  </span>
                </div>

                <p className="text-lg font-bold text-slate-900 mt-2">
                  {kpis.externalPct}
                </p>

                <p className="text-xs text-slate-500">
                  Blockers involving external dependencies
                </p>
              </div>

              {/* Resolution Rate */}
              <div className="bg-white border border-slate-200 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500">
                    Delivery Completion
                  </span>

                  <span
                    className={`text-xs font-bold px-2 py-1 rounded-full ${
                      parseFloat(kpis.rate) >= 70
                        ? 'bg-emerald-100 text-emerald-700'
                        : 'bg-amber-100 text-amber-700'
                    }`}
                  >
                    {parseFloat(kpis.rate) >= 70
                      ? 'Healthy'
                      : 'Needs Attention'}
                  </span>
                </div>

                <p className="text-lg font-bold text-slate-900 mt-2">
                  {kpis.rate}
                </p>

                <p className="text-xs text-slate-500">
                  Blocker resolution rate
                </p>
              </div>

            </div>
          </div>
        </section>

        {/* NAVIGATION TABS */}
        <div className="bg-white border-b border-slate-200 px-6 pt-3">
          <div className="max-w-7xl mx-auto flex gap-8">
            <button
              onClick={() => setActiveTab('overview')}
              className={`pb-3 text-sm font-medium border-b-2 transition ${activeTab === 'overview' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'
                }`}
            >
              Blocker Analysis
            </button>
            <button
              onClick={() => setActiveTab('trends')}
              className={`pb-3 text-sm font-medium border-b-2 transition ${activeTab === 'trends' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'
                }`}
            >
              Delivery Trend Analysis
            </button>
            <button
              onClick={() => setActiveTab('rootcause')}
              className={`pb-3 text-sm font-medium border-b-2 transition ${activeTab === 'rootcause' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'
                }`}
            >
              Root Cause & Recommendation Cards
            </button>
            <button
              onClick={() => setActiveTab('explorer')}
              className={`pb-3 text-sm font-medium border-b-2 transition ${activeTab === 'explorer' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'
                }`}
            >
              Data Explorer ({filteredData.length})
            </button>
          </div>
        </div>

        {/* TAB CONTENTS */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-50">
          <div className="max-w-7xl mx-auto space-y-6">

            {/* TAB 1: OVERVIEW & BLOCKER ANALYSIS */}
            {activeTab === 'overview' && (
              <div className="grid grid-cols-2 gap-6">

                {/* Category Distribution Bar Chart */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <Layers className="w-4 h-4 text-blue-600" />
                    Blocker Category Distribution
                  </h3>
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={categoryChartData} layout="vertical" margin={{ left: 40, right: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#F1F5F9" />
                        <XAxis type="number" stroke="#64748B" fontSize={12} />
                        <YAxis dataKey="name" type="category" stroke="#64748B" fontSize={11} width={130} />
                        <Tooltip contentStyle={{ backgroundColor: '#1E293B', color: '#FFF', borderRadius: '8px', border: 'none' }} />
                        <Bar dataKey="count" fill={COLOR_PALETTE.primary} radius={[0, 4, 4, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Internal vs External Donut Chart */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <ShieldAlert className="w-4 h-4 text-amber-600" />
                    External Dependency Breakdown
                  </h3>
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={dependencyChartData}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={95}
                          paddingAngle={3}
                          dataKey="value"
                          label={({ name, percent }: { name?: string; percent?: number }) => `${name}: ${((percent ?? 0) * 100).toFixed(0)}%`}
                        >
                          {dependencyChartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip contentStyle={{ backgroundColor: '#1E293B', color: '#FFF', borderRadius: '8px', border: 'none' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Team Volume Bar Chart */}
                <div className="col-span-2 bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <Users className="w-4 h-4 text-blue-600" />
                    Team-wise Blocker Volume Comparison
                  </h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={teamChartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                        <XAxis dataKey="name" stroke="#64748B" fontSize={12} />
                        <YAxis stroke="#64748B" fontSize={12} />
                        <Tooltip contentStyle={{ backgroundColor: '#1E293B', color: '#FFF', borderRadius: '8px', border: 'none' }} />
                        <Bar dataKey="count" fill={COLOR_PALETTE.primary} radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

              </div>
            )}

            {/* TAB 2: DELIVERY TREND ANALYSIS */}
            {activeTab === 'trends' && (
              <div className="space-y-6">

                {/* Trend Line Chart */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <h3 className="text-base font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-blue-600" />
                    Daily Blocker Logging Trend
                  </h3>
                  <div className="h-80">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={trendChartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                        <XAxis dataKey="date" stroke="#64748B" fontSize={12} />
                        <YAxis stroke="#64748B" fontSize={12} />
                        <Tooltip contentStyle={{ backgroundColor: '#1E293B', color: '#FFF', borderRadius: '8px', border: 'none' }} />
                        <Line type="monotone" dataKey="count" stroke={COLOR_PALETTE.primary} strokeWidth={3} dot={{ r: 4 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Sprint vs Category Matrix */}
                <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                  <h3 className="text-base font-bold text-slate-900 mb-4">Sprint Bottleneck Analysis Matrix</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left text-slate-700">
                      <thead className="text-xs uppercase bg-slate-100 text-slate-600">
                        <tr>
                          <th className="px-4 py-3">Sprint Cycle</th>
                          {allCategories.map(cat => <th key={cat} className="px-4 py-3">{cat}</th>)}
                        </tr>
                      </thead>
                      <tbody>
                        {sprintCategoryHeatmapData.map((row: any) => (
                          <tr key={row.sprint} className="border-b border-slate-100 hover:bg-slate-50">
                            <td className="px-4 py-3 font-semibold text-slate-900">{row.sprint}</td>
                            {allCategories.map(cat => {
                              const val = row[cat] || 0;
                              const bg = val > 5 ? 'bg-red-100 text-red-700 font-bold' : val > 2 ? 'bg-amber-100 text-amber-700' : 'bg-slate-50 text-slate-600';
                              return (
                                <td key={cat} className="px-4 py-3">
                                  <span className={`px-2.5 py-1 rounded-md text-xs ${bg}`}>{val}</span>
                                </td>
                              );
                            })}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

              </div>
            )}

           {/* TAB 3: BUSINESS INSIGHTS & RECOMMENDATIONS */}
{activeTab === 'rootcause' && (
  <div className="space-y-6">

    {/* Section Header */}
    <div>
      <h2 className="text-xl font-bold text-slate-900">
        Business Insights & Recommendations
      </h2>

      <p className="text-sm text-slate-500 mt-1">
        Data-driven observations based on the currently selected
        teams, sprints, categories, and statuses.
      </p>
    </div>

    {/* Executive Summary */}
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-5">

      <div className="flex items-start gap-3">

        <TrendingUp className="w-5 h-5 text-blue-600 mt-1" />

        <div>

          <h3 className="font-bold text-blue-900 text-base">
            Executive Summary
          </h3>

          <p className="text-sm text-blue-800 mt-2 leading-relaxed">

            The current filtered dataset contains{' '}
            <b>{kpis.total}</b> blockers with a resolution rate of{' '}
            <b>{kpis.rate}</b>.

            The most frequent blocker category is{' '}
            <b>{kpis.topCategory}</b>, while{' '}
            <b>{kpis.topTeam}</b> has the highest blocker volume.

            External dependencies account for{' '}
            <b>{kpis.externalPct}</b> of the currently selected blockers.

          </p>

        </div>

      </div>

    </div>


    {/* INSIGHT CARDS */}
    <div className="grid grid-cols-2 gap-5">

      {/* Insight 1 - External Dependencies */}
      <div className="bg-white border-l-4 border-amber-500 border-y border-r border-slate-200 rounded-xl p-5 shadow-sm">

        <div className="flex justify-between items-start">

          <div className="flex items-start gap-3">

            <div className="bg-amber-50 p-2 rounded-lg">
              <ShieldAlert className="w-5 h-5 text-amber-600" />
            </div>

            <div>

              <h3 className="font-bold text-slate-900">
                External Dependency Risk
              </h3>

              <span className="inline-block mt-2 text-xs font-semibold bg-amber-100 text-amber-700 px-2.5 py-1 rounded-full">
                High Impact
              </span>

            </div>

          </div>

          <p className="text-xl font-bold text-slate-900">
            {kpis.externalPct}
          </p>

        </div>


        <div className="mt-5">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Observation
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            External dependencies represent{' '}
            <b>{kpis.externalPct}</b> of the blockers in the current
            filtered dataset.

          </p>

        </div>


        <div className="mt-4">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Business Impact
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            Dependency-driven blockers can increase coordination
            overhead and create delays across sprint boundaries.

          </p>

        </div>


        <div className="mt-4 pt-4 border-t border-slate-100">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Recommended Action
          </p>

          <p className="text-sm font-semibold text-slate-800 mt-1 leading-relaxed">

            Establish clear ownership, escalation paths, and
            cross-team SLAs for external dependencies.

          </p>

        </div>

      </div>


      {/* Insight 2 - Top Team */}
      <div className="bg-white border-l-4 border-red-500 border-y border-r border-slate-200 rounded-xl p-5 shadow-sm">

        <div className="flex justify-between items-start">

          <div className="flex items-start gap-3">

            <div className="bg-red-50 p-2 rounded-lg">
              <Users className="w-5 h-5 text-red-600" />
            </div>

            <div>

              <h3 className="font-bold text-slate-900">
                Team With Highest Blocker Volume
              </h3>

              <span className="inline-block mt-2 text-xs font-semibold bg-red-100 text-red-700 px-2.5 py-1 rounded-full">
                Critical Bottleneck
              </span>

            </div>

          </div>

          <p className="text-xl font-bold text-slate-900">
            {kpis.topTeamCount}
          </p>

        </div>


        <div className="mt-5">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Observation
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            <b>{kpis.topTeam}</b> has the highest blocker volume
            with <b>{kpis.topTeamCount}</b> recorded issues.

          </p>

        </div>


        <div className="mt-4">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Business Impact
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            A high concentration of blockers within one team may
            indicate recurring process, tooling, or dependency
            problems.

          </p>

        </div>


        <div className="mt-4 pt-4 border-t border-slate-100">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Recommended Action
          </p>

          <p className="text-sm font-semibold text-slate-800 mt-1 leading-relaxed">

            Review the team's recurring blocker categories during
            retrospectives and identify preventable causes.

          </p>

        </div>

      </div>


      {/* Insight 3 - Resolution Performance */}
      <div className="bg-white border-l-4 border-blue-500 border-y border-r border-slate-200 rounded-xl p-5 shadow-sm">

        <div className="flex justify-between items-start">

          <div className="flex items-start gap-3">

            <div className="bg-blue-50 p-2 rounded-lg">
              <Clock className="w-5 h-5 text-blue-500" />
{categoryResolution.category} has the highest resolution time
            </div>

            <div>

              <h3 className="font-bold text-slate-900">
                Resolution Performance
              </h3>

              <span className="inline-block mt-2 text-xs font-semibold bg-blue-100 text-blue-700 px-2.5 py-1 rounded-full">
                Operational KPI
              </span>

            </div>

          </div>

          <p className="text-xl font-bold text-slate-900">
            {kpis.avgResolution}
          </p>

        </div>


        <div className="mt-5">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Observation
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            Blockers currently require an average of{' '}
            <b>{kpis.avgResolution}</b> to resolve.

          </p>

        </div>


        <div className="mt-4">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Business Impact
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            Longer resolution cycles can increase sprint spillover
            and reduce delivery predictability.

          </p>

        </div>


        <div className="mt-4 pt-4 border-t border-slate-100">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Recommended Action
          </p>

          <p className="text-sm font-semibold text-slate-800 mt-1 leading-relaxed">

            Prioritize ageing blockers and introduce escalation
            rules for issues that remain unresolved beyond the
            expected SLA.

          </p>

        </div>

      </div>


      {/* Insight 4 - Top Category */}
      <div className="bg-white border-l-4 border-indigo-500 border-y border-r border-slate-200 rounded-xl p-5 shadow-sm">

        <div className="flex justify-between items-start">

          <div className="flex items-start gap-3">

            <div className="bg-indigo-50 p-2 rounded-lg">
              <Layers className="w-5 h-5 text-indigo-600" />
            </div>

            <div>

              <h3 className="font-bold text-slate-900">
                Dominant Blocker Category
              </h3>

              <span className="inline-block mt-2 text-xs font-semibold bg-indigo-100 text-indigo-700 px-2.5 py-1 rounded-full">
                Root Cause Signal
              </span>

            </div>

          </div>

          <p className="text-xl font-bold text-slate-900">
            {kpis.topCategoryCount}
          </p>

        </div>


        <div className="mt-5">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Observation
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            <b>{kpis.topCategory}</b> is the most frequently occurring
            blocker category with <b>{kpis.topCategoryCount}</b>{' '}
            incidents.

          </p>

        </div>


        <div className="mt-4">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Business Impact
          </p>

          <p className="text-sm text-slate-700 mt-1 leading-relaxed">

            Repeated occurrences suggest a potential systemic
            bottleneck rather than isolated sprint friction.

          </p>

        </div>


        <div className="mt-4 pt-4 border-t border-slate-100">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Recommended Action
          </p>

          <p className="text-sm font-semibold text-slate-800 mt-1 leading-relaxed">

            Investigate the recurring causes of{' '}
            <b>{kpis.topCategory}</b> and introduce preventive
            documentation, automation, or process improvements.

          </p>

        </div>

      </div>

    </div>


    {/* LEADERSHIP DECISION SUPPORT */}

    <div className="bg-white border border-slate-200 rounded-xl p-5">

      <div className="flex items-center gap-2 mb-4">

        <ShieldAlert className="w-5 h-5 text-indigo-600" />

        <h3 className="font-bold text-slate-900">
          Leadership Decision Support
        </h3>

      </div>

      <div className="grid grid-cols-3 gap-4">

        <div className="bg-slate-50 rounded-lg p-4">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Priority Area
          </p>

          <p className="font-bold text-slate-900 mt-1">
            {kpis.topCategory}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Highest blocker concentration
          </p>

        </div>


        <div className="bg-slate-50 rounded-lg p-4">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Team Focus
          </p>

          <p className="font-bold text-slate-900 mt-1">
            {kpis.topTeam}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Highest blocker volume
          </p>

        </div>


        <div className="bg-slate-50 rounded-lg p-4">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Resolution Performance
          </p>

          <p className="font-bold text-slate-900 mt-1">
            {kpis.avgResolution}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Average blocker resolution time
          </p>

        </div>

      </div>

    </div>

  </div>
)}

            {/* TAB 4: DATA EXPLORER */}
            {activeTab === 'explorer' && (
              <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4">

                <div className="flex justify-between items-center">
                  <div className="relative w-80">
                    <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                    <input
                      type="text"
                      placeholder="Search descriptions, IDs..."
                      value={searchTerm}
                      onChange={e => setSearchTerm(e.target.value)}
                      className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <span className="text-xs text-slate-500">Showing {filteredData.length} records</span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-sm text-left text-slate-700">
                    <thead className="text-xs uppercase bg-slate-100 text-slate-600">
                      <tr>
                        <th className="px-4 py-3">Blocker ID</th>
                        <th className="px-4 py-3">Team</th>
                        <th className="px-4 py-3">Sprint</th>
                        <th className="px-4 py-3">Date Logged</th>
                        <th className="px-4 py-3">Category</th>
                        <th className="px-4 py-3">External?</th>
                        <th className="px-4 py-3">Resolution (Days)</th>
                        <th className="px-4 py-3">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredData.map(item => (
                        <tr key={item.blocker_id} className="border-b border-slate-100 hover:bg-slate-50">
                          <td className="px-4 py-3 font-semibold text-blue-600">{item.blocker_id}</td>
                          <td className="px-4 py-3">{item.team_id}</td>
                          <td className="px-4 py-3">{item.sprint_id}</td>
                          <td className="px-4 py-3">{item.date_logged}</td>
                          <td className="px-4 py-3">{item.category}</td>
                          <td className="px-4 py-3">
                            {item.is_external_dependency ? (
                              <span className="bg-amber-100 text-amber-800 text-xs px-2 py-0.5 rounded-full font-medium">Yes</span>
                            ) : (
                              <span className="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded-full font-medium">No</span>
                            )}
                          </td>
                          <td className="px-4 py-3 font-medium">{item.resolution_time_days}d</td>
                          <td className="px-4 py-3">
                            <span className="bg-emerald-100 text-emerald-800 text-xs px-2 py-0.5 rounded-full font-medium">{item.status}</span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

              </div>
            )}

          </div>
        </div>

      </main>

    </div>
  );
}