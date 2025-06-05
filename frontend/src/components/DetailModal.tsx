import React from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  Text,
  Stack,
  Tag,
  Wrap,
  WrapItem,
} from '@chakra-ui/react';
import { Resource } from './ResourceCard';

interface DetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  resource: Resource;
}

/**
 * Modal displaying detailed information about a resource.
 */
const DetailModal: React.FC<DetailModalProps> = ({ isOpen, onClose, resource }) => (
  <Modal isOpen={isOpen} onClose={onClose} size="lg">
    <ModalOverlay />
    <ModalContent>
      <ModalHeader>{resource.name}</ModalHeader>
      <ModalCloseButton />
      <ModalBody>
        {resource.description && <Text mb={4}>{resource.description}</Text>}
        {resource.tags && resource.tags.length > 0 && (
          <Wrap mb={4}>
            {resource.tags.map((tag) => (
              <WrapItem key={tag}>
                <Tag>{tag}</Tag>
              </WrapItem>
            ))}
          </Wrap>
        )}
        {resource.partners && resource.partners.length > 0 && (
          <Stack spacing={1} fontSize="sm" color="gray.600">
            <Text fontWeight="bold">Partners Involved</Text>
            <Text>{resource.partners.join(', ')}</Text>
          </Stack>
        )}
      </ModalBody>
      <ModalFooter>
        <Button onClick={onClose}>Close</Button>
      </ModalFooter>
    </ModalContent>
  </Modal>
);

export default DetailModal;
