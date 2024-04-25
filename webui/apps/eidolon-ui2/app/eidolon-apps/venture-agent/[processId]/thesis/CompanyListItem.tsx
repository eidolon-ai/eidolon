import * as React from "react";
import {Avatar, Backdrop, CircularProgress, IconButton, ImageListItem, ImageListItemBar, Paper} from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";
import {Company} from "../../types";

export interface CompanyListItemProps {
  item: Company
  selectedCompany?: Company
  selectCompany: (company: Company) => void
}

export function CompanyListItem({item, selectCompany, selectedCompany}: CompanyListItemProps) {
  function stringAvatar(name: string) {
    return {
      sx: {
        width: 180,
        height: 180,
      },
      children: `${name.split(' ')[0]?.[0]}${name.split(' ')[1]?.[0] || ''}`,
    };
  }

  let itemBarOptions: Record<string, any> = {
    alignItems: 'end'
  }

  return (
    <Paper
      sx={{position: "relative", border: '1px solid #ccc', width: 'fit-content', height: 'fit-content'}}
    >
      <Backdrop
        sx={{position: 'absolute', color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}}
        open={item.loading}
      >
        <CircularProgress color="inherit"/>
      </Backdrop>
      <ImageListItem key={item.name}
                     sx={{width: 180, height: 180}}
      >
        <Avatar
          variant="square"
          src={item.researched_details?.logo_url}
          {...stringAvatar(item.name)}
        />
        <ImageListItemBar
          sx={itemBarOptions}
          title={item.name}
          subtitle={item.category}
          actionIcon={
            <IconButton
              sx={{color: selectedCompany?.name === item.name ? 'rgba(50, 50, 255, 0.54)' : 'rgba(255, 255, 255, 0.54)'}}
              aria-label={`info about ${item.name}`}
              onClick={() => selectCompany(item)}
            >
              <InfoIcon/>
            </IconButton>
          }
        >
        </ImageListItemBar>
      </ImageListItem>
    </Paper>
  )
}