import React, { useEffect, useState } from 'react';
import {
  Box,
  FormControl,
  FormLabel,
  Input,
  Select,
  Checkbox,
  CheckboxGroup,
  HStack,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  VStack,
} from '@chakra-ui/react';

import type { SearchFilters } from '../utils/api';

type FiltersState = SearchFilters;

interface FiltersProps {
  onFilterChange: (filters: SearchFilters) => void;
}

const counties = ['County A', 'County B', 'County C'];
const insuranceTypes = ['Private', 'Medicaid', 'None'];
const systems = ['Education', 'Healthcare', 'Housing'];

const Filters: React.FC<FiltersProps> = ({ onFilterChange }) => {
  const [filters, setFilters] = useState<FiltersState>({
    age: 0,
    county: '',
    insurance: '',
    system: [],
    keyword: '',
  });

  useEffect(() => {
    onFilterChange(filters);
  }, [filters, onFilterChange]);

  return (
    <Box p={4} borderWidth="1px" borderRadius="md">
      <VStack spacing={4} align="stretch">
        <FormControl>
          <FormLabel>Age</FormLabel>
          <Slider
            aria-label="age-slider"
            min={0}
            max={100}
            value={filters.age}
            onChange={(val) => setFilters((f) => ({ ...f, age: val }))}
          >
            <SliderTrack>
              <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb />
          </Slider>
        </FormControl>

        <FormControl>
          <FormLabel>County</FormLabel>
          <Select
            placeholder="Select county"
            value={filters.county}
            onChange={(e) =>
              setFilters((f) => ({ ...f, county: e.target.value }))
            }
          >
            {counties.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </Select>
        </FormControl>

        <FormControl>
          <FormLabel>Insurance</FormLabel>
          <Select
            placeholder="Select insurance"
            value={filters.insurance}
            onChange={(e) =>
              setFilters((f) => ({ ...f, insurance: e.target.value }))
            }
          >
            {insuranceTypes.map((i) => (
              <option key={i} value={i}>
                {i}
              </option>
            ))}
          </Select>
        </FormControl>

        <FormControl>
          <FormLabel>System</FormLabel>
          <CheckboxGroup
            value={filters.system}
            onChange={(values) =>
              setFilters((f) => ({ ...f, system: values as string[] }))
            }
          >
            <HStack spacing={4}>
              {systems.map((s) => (
                <Checkbox key={s} value={s}>
                  {s}
                </Checkbox>
              ))}
            </HStack>
          </CheckboxGroup>
        </FormControl>

        <FormControl>
          <FormLabel>Keyword</FormLabel>
          <Input
            placeholder="Search keyword"
            value={filters.keyword}
            onChange={(e) =>
              setFilters((f) => ({ ...f, keyword: e.target.value }))
            }
          />
        </FormControl>
      </VStack>
    </Box>
  );
};

export default Filters;
