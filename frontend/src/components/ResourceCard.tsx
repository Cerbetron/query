import React from 'react';
import {
  Box,
  Heading,
  Text,
  Stack,
  Tag,
  Wrap,
  WrapItem,
  Button,
  useDisclosure,
} from '@chakra-ui/react';
import DetailModal from './DetailModal';

export interface Resource {
  id: number;
  name: string;
  description?: string;
  tags?: string[];
  partners?: string[];
}

interface ResourceCardProps {
  resource: Resource;
}

/**
 * Display a summary card for a resource with a details modal.
 */
const ResourceCard: React.FC<ResourceCardProps> = ({ resource }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Box borderWidth="1px" borderRadius="md" p={4}>
      <Stack spacing={3}>
        <Heading size="md">{resource.name}</Heading>
        {resource.description && (
          <Text noOfLines={2}>{resource.description}</Text>
        )}
        {resource.tags && resource.tags.length > 0 && (
          <Wrap>
            {resource.tags.map((tag) => (
              <WrapItem key={tag}>
                <Tag>{tag}</Tag>
              </WrapItem>
            ))}
          </Wrap>
        )}
        {resource.partners && resource.partners.length > 0 && (
          <Text fontSize="sm" color="gray.600">
            Partners: {resource.partners.join(', ')}
          </Text>
        )}
        <Button alignSelf="start" onClick={onOpen} size="sm" colorScheme="blue">
          Details
        </Button>
      </Stack>
      <DetailModal isOpen={isOpen} onClose={onClose} resource={resource} />
    </Box>
  );
};

export default ResourceCard;
