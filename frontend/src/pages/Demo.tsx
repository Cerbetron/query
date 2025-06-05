import React, { useState } from 'react';
import { Button, Spinner, Text, VStack } from '@chakra-ui/react';
import ResourceList from '../components/ResourceList';
import { searchResources, type Resource, type SearchFilters } from '../utils/api';

// List of predefined demo searches. Each label corresponds to filters passed
// to the search API when the button is clicked.
const demos: { label: string; filters: SearchFilters }[] = [
  { label: 'wraparound for teens', filters: { keyword: 'wraparound', tags: ['teens'] } },
  { label: 'residential services in Alameda', filters: { keyword: 'residential', county: 'Alameda' } },
  { label: 'drop in centers', filters: { keyword: 'drop in center' } },
  { label: 'bilingual therapy', filters: { keyword: 'bilingual therapy' } },
  { label: 'family support groups', filters: { keyword: 'family support' } },
];

/**
 * Demo page that exposes a set of predefined searches. Clicking a button will
 * execute the corresponding search and display the results below.
 */
const Demo: React.FC = () => {
  const [results, setResults] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runDemo = async (filters: SearchFilters) => {
    setLoading(true);
    setError(null);
    try {
      const data = await searchResources(filters);
      setResults(data);
    } catch (_) {
      setError('Failed to load resources');
    } finally {
      setLoading(false);
    }
  };

  return (
    <VStack spacing={4} align="stretch" p={4}>
      {demos.map((demo) => (
        <Button key={demo.label} onClick={() => runDemo(demo.filters)}>
          {demo.label}
        </Button>
      ))}
      {loading && <Spinner alignSelf="center" />}
      {error && (
        <Text color="red.500" textAlign="center">
          {error}
        </Text>
      )}
      {!loading && !error && results.length > 0 && (
        <ResourceList resources={results} />
      )}
    </VStack>
  );
};

export default Demo;
