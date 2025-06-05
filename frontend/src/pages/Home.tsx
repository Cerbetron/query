import React, { useCallback, useEffect, useState } from 'react';
import { Spinner, Text, VStack } from '@chakra-ui/react';
import Filters from '../components/Filters';
import ResourceList from '../components/ResourceList';
import { searchResources, type SearchFilters, type Resource } from '../utils/api';

/**
 * Home page showing Filters and search results. Results are fetched
 * from the backend whenever filter values change.
 */
const Home: React.FC = () => {
  const [filters, setFilters] = useState<SearchFilters>({});
  const [results, setResults] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchResults = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await searchResources(filters);
      setResults(data);
    } catch (err) {
      setError('Failed to load resources');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchResults();
  }, [fetchResults]);

  return (
    <VStack spacing={4} align="stretch" p={4}>
      <Filters onFilterChange={setFilters} />
      {loading && <Spinner alignSelf="center" />}
      {error && (
        <Text color="red.500" textAlign="center">
          {error}
        </Text>
      )}
      {!loading && !error && <ResourceList resources={results} />}
    </VStack>
  );
};

export default Home;
