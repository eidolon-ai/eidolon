import React from 'react';
import {Box, Button, IconButton, Typography} from '@mui/material';
import {Company} from "../../types";
import {CompanyListItem} from "./CompanyListItem";
import {Image, ImageRounded} from "@mui/icons-material";
import harmonicStamp from "./harmonic_stamp.svg"

interface CompanyDetailsProps {
  company: Company;
  refreshResearch: (company: Company) => void;
}

const CompanyDetailsLayout: React.FC<CompanyDetailsProps> = ({company, refreshResearch}) => {
  const {name, category, researched_details: details} = company;

  return (
    <Box sx={{padding: '16px 32px 16px 32px', overflow: "auto"}}>
      <Box>
        <Box sx={{float: "right", display: "flex", alignItems: "start"}}>
          <CompanyListItem item={company}/>
        </Box>
        <Typography variant="h5" component="div" paragraph>
          <Box sx={{display: "flex", flexDirection: "flow"}}>
            <Box>
              <Typography
                variant="h4"
              >
                {name}
                {company.researched_details?.enriched_with_harmonic &&
                    <IconButton href="https://www.harmonic.ai" style={{marginTop: "-24px", marginLeft: "-16px", opacity: "0.9", zIndex: 99}}>
                        <img src={harmonicStamp.src} style={{height: "64px", width: "64px"}}/>
                    </IconButton>
                }
              </Typography>
              <Typography
                sx={{marginLeft: '12px'}}
                variant="subtitle1" color="textSecondary"
              >
                {details?.description}
              </Typography>
            </Box>
          </Box>
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Category:</strong> {category}
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Stage:</strong> {details?.stage}
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Market Size:</strong> {details?.market_size}
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Business Model:</strong> {details?.business_model}
        </Typography>
        {details?.other_information && (
          <Typography variant="body1" paragraph>
            <strong>Other Information:</strong> {details?.other_information}
          </Typography>
        )}
      </Box>
    </Box>
  );
};

export default CompanyDetailsLayout
