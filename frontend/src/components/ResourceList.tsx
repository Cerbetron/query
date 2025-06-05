import React from 'react';
import { SimpleGrid, Text } from '@chakra-ui/react';
import ResourceCard from './ResourceCard';
import type { Resource } from '../utils/api';

interface ResourceListProps {
  resources: Resource[];
}

const ResourceList: React.FC<ResourceListProps> = ({ resources }) => {
  if (!resources || resources.length === 0) {
    return <Text>No resources found.</Text>;
  }

  return (
    <SimpleGrid spacing={4} columns={{ base: 1, md: 2, lg: 3 }}>
      {resources.map((res) => (
        <ResourceCard key={res.id} resource={res} />
      ))}
    </SimpleGrid>
  );
};

export default ResourceList;
