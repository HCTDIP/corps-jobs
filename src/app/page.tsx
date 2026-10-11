'use client';

import { useState } from 'react';

interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  type: string;
  salary: string;
  posted: string;
  description: string;
}

const jobs: Job[] = [
  {
    id: 1,
    title: 'Senior Frontend Developer',
    company: 'TechCorp',
    location: 'Remote',
    type: 'Full-time',
    salary: '$120k - $150k',
    posted: '2 days ago',
    description: 'We are looking for an experienced frontend developer...',
  },
  {
    id: 2,
    title: 'Backend Engineer',
    company: 'DataFlow',
    location: 'New York, NY',
    type: 'Full-time',
    salary: '$130k - $160k',
    posted: '1 day ago',
    description: 'Join our backend team to build scalable APIs...',
  },
  {
    id: 3,
    title: 'Product Designer',
    company: 'DesignHub',
    location: 'San Francisco, CA',
    type: 'Remote',
    salary: '$100k - $130k',
    posted: '3 days ago',
    description: 'Create beautiful and intuitive user experiences...',
  },
];

export default function Home() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState('All');
  const [selectedLocation, setSelectedLocation] = useState('All');
  const [filteredJobs, setFilteredJobs] = useState(jobs);
  const [appliedJobs, setAppliedJobs] = useState<number[]>([]);

  const types = ['All', 'Full-time', 'Part-time', 'Contract', 'Remote'];
  const locations = ['All', 'Remote', 'New York, NY', 'San Francisco, CA', 'London, UK'];

  useState(() => {
    const results = jobs.filter((job) => {
      const matchesSearch =
        job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.company.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = selectedType === 'All' || job.type === selectedType;
      const matchesLocation = selectedLocation === 'All' || job.location === selectedLocation;
      return matchesSearch && matchesType && matchesLocation;
    });
    setFilteredJobs(results);
  }, [searchTerm, selectedType, selectedLocation]);

  const handleApply = (jobId: number) => {
    setAppliedJobs((prev) => [...prev, jobId]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Corps Jobs</h1>
          <p className="text-gray-600 mt-2">Find your dream job today</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row gap-6 mb-8">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search jobs..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="flex gap-4">
            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
            >
              {types.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={selectedLocation}
              onChange={(e) => setSelectedLocation(e.target.value)}
            >
              {locations.map((loc) => (
                <option key={loc} value={loc}>
                  {loc}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid gap-4">
          {filteredJobs.map((job) => (
            <div
              key={job.id}
              className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">{job.title}</h2>
                  <p className="text-gray-600 mt-1">{job.company} · {job.location}</p>
                  <div className="flex gap-4 mt-2">
                    <span className="text-sm text-gray-500">{job.type}</span>
                    <span className="text-sm text-gray-500">{job.salary}</span>
                    <span className="text-sm text-gray-500">{job.posted}</span>
                  </div>
                  <p className="text-gray-700 mt-3">{job.description}</p>
                </div>
                <button
                  onClick={() => handleApply(job.id)}
                  disabled={appliedJobs.includes(job.id)}
                  className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                    appliedJobs.includes(job.id)
                      ? 'bg-green-100 text-green-700 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {appliedJobs.includes(job.id) ? 'Applied' : 'Apply Now'}
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredJobs.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No jobs found matching your criteria.</p>
          </div>
        )}
      </main>
    </div>
  );
}
