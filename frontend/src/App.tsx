import React, { useState } from 'react';
import { ChakraProvider, Box, Container } from '@chakra-ui/react';
import Filters from './components/Filters';
import ResourceList from './components/ResourceList';

/**
 * Main App layout using Chakra UI.
 * Renders Filters component and below it the ResourceList.
 * useState is used to track filter values and search results.
 */
const App: React.FC = () => {
  // Track the currently selected filters
  const [filters, setFilters] = useState<Record<string, string | string[]>>({});
  // Hold the resources returned from the API or filter logic
  const [results, setResults] = useState<any[]>([]);

  return (
    <ChakraProvider>
      <Container maxW="container.xl" py={4}>
        <Box mb={4}>
          <Filters filters={filters} setFilters={setFilters} onSearch={setResults} />
        </Box>
        <ResourceList resources={results} />
      </Container>
    </ChakraProvider>
  );
};

export default App;
