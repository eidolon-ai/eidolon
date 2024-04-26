import React from 'react';
import {Box, Button, Grid, Typography} from '@mui/material';
import {Company} from "../../types";

interface CompanyDetailsProps {
  company: Company;
  refreshResearch: (company: Company) => void;
}

const CompanyDetailsLayout: React.FC<CompanyDetailsProps> = ({company, refreshResearch}) => {
  const {name, category, researched_details: details} = company;

  return (
    <Box sx={{padding: '16px 32px 16px 32px', height: 'calc(100% - 32px)', overflowY: "auto"}}>
      <Box>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="h5" component="div">
              <Box
                sx={{display: 'flex', justifyContent: 'space-between'}}
              >
                {name} <Button onClick={() => refreshResearch(company)}>Refresh Information</Button>
              </Box>
            </Typography>
            <Typography
              sx={{marginLeft: '12px'}}
              variant="subtitle1" color="textSecondary">
              {details?.description}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Category:</strong> {category}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Stage:</strong> {details?.stage}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Market Size:</strong> {details?.market_size}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              <strong>Business Model:</strong> {details?.business_model}
            </Typography>
          </Grid>
          {details?.other_information && (
            <Grid item xs={12}>
              <Typography variant="body1">
                <strong>Other Information:</strong> {details?.other_information}
              </Typography>
            </Grid>
          )}
        </Grid>
      </Box>
    </Box>
  );
};

export default CompanyDetailsLayout
