import TextField from "@mui/material/TextField";
import Autocomplete, { createFilterOptions } from "@mui/material/Autocomplete";
import type { TeleportLocation } from '../types';

interface GroupedSelectProps {
  locations: TeleportLocation[];
  selectedLocation: TeleportLocation | null;
  onLocationSelect: (location: TeleportLocation | null) => void;
  disabled?: boolean;
}

// Custom filter that searches both displayName and category
const filter = createFilterOptions<TeleportLocation>();

export default function GroupedSelect({ 
  locations, 
  selectedLocation, 
  onLocationSelect, 
  disabled = false 
}: GroupedSelectProps) {
  return (
    <Autocomplete
      options={locations}
      groupBy={(option) => option.category || 'Other'}
      getOptionLabel={(option) => option.displayName}
      value={selectedLocation}
      onChange={(_, value) => onLocationSelect(value)}
      disabled={disabled}
      sx={{ 
        width: '100%',
        '& .MuiInputBase-root': {
          backgroundColor: '#252526',
          border: '1px solid #3c3c3c',
          borderRadius: '3px',
          color: '#ffffff',
          fontSize: '14px',
          '&:hover': {
            borderColor: '#569cd6',
          },
          '&.Mui-focused': {
            borderColor: '#569cd6',
            boxShadow: 'none',
          },
        },
        '& .MuiInputBase-input': {
          color: '#ffffff',
          padding: '8px 12px',
        },
        '& .MuiInputLabel-root': {
          color: '#cccccc',
          fontSize: '14px',
          '&.Mui-focused': {
            color: '#569cd6',
          },
        },
        '& .MuiOutlinedInput-notchedOutline': {
          border: 'none',
        },
        '& .MuiAutocomplete-endAdornment': {
          '& .MuiButtonBase-root': {
            color: '#cccccc',
          },
        },
      }}
      componentsProps={{
        paper: {
          sx: {
            backgroundColor: '#252526',
            border: '1px solid #3c3c3c',
            borderRadius: '0 0 3px 3px',
            maxHeight: '300px',
            '& .MuiAutocomplete-listbox': {
              padding: 0,
              '& .MuiAutocomplete-option': {
                backgroundColor: '#252526',
                color: '#ffffff',
                padding: '8px 12px',
                fontSize: '14px',
                borderBottom: '1px solid #3c3c3c',
                '&:hover': {
                  backgroundColor: '#2d2d30',
                },
                '&[aria-selected="true"]': {
                  backgroundColor: '#0e639c',
                  '&:hover': {
                    backgroundColor: '#1177bb',
                  },
                },
              },
              '& .MuiAutocomplete-groupLabel': {
                backgroundColor: '#2d2d30',
                color: '#569cd6',
                fontWeight: 'bold',
                fontSize: '12px',
                padding: '8px 12px',
                textTransform: 'uppercase',
                letterSpacing: '0.5px',
                borderBottom: '1px solid #3c3c3c',
                position: 'sticky',
                top: 0,
                zIndex: 1,
              },
            },
          },
        },
      }}
      filterOptions={(options, params) => {
        const filtered = filter(options, params);
        
        // Also search by category name
        const { inputValue } = params;
        if (inputValue !== '') {
          const categoryMatches = options.filter((option) =>
            (option.category || '').toLowerCase().includes(inputValue.toLowerCase())
          );
          
          // Combine filtered results with category matches (remove duplicates)
          const combined = [...filtered];
          categoryMatches.forEach(match => {
            if (!combined.find(item => item.id === match.id)) {
              combined.push(match);
            }
          });
          
          return combined;
        }
        
        return filtered;
      }}
      renderInput={(params) => (
        <TextField {...params} label="Select Teleport Location" />
      )}
    />
  );
}
