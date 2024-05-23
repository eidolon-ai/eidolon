import * as React from 'react';
import {alpha} from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import FilterListIcon from '@mui/icons-material/FilterList';
import {Button} from "@mui/material";
import {Company} from "../../types";

type Order = 'asc' | 'desc';

interface HeadCell {
  disablePadding: boolean;
  id: keyof Company;
  label: string;
  numeric: boolean;
}

const headCells: readonly HeadCell[] = [
  {
    id: 'name',
    numeric: false,
    disablePadding: true,
    label: 'Company Name',
  },
  {
    id: 'category',
    numeric: true,
    disablePadding: false,
    label: 'Category',
  },
];

interface EnhancedTableProps {
  numSelected: number;
  onRequestSort: (event: React.MouseEvent<unknown>, property: keyof Company) => void;
  onSelectAllClick: (event: React.ChangeEvent<HTMLInputElement>) => void;
  order: Order;
  orderBy: string;
  rowCount: number;
}

function EnhancedTableHead(props: EnhancedTableProps) {
  const {onSelectAllClick, order, orderBy, numSelected, rowCount, onRequestSort} =
    props;
  const createSortHandler =
    (property: keyof Company) => (event: React.MouseEvent<unknown>) => {
      onRequestSort(event, property);
    };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            color="primary"
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{
              'aria-label': 'select all desserts',
            }}
          />
        </TableCell>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? 'right' : 'left'}
            padding={headCell.disablePadding ? 'none' : 'normal'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

interface EnhancedTableToolbarProps {
  numSelected: number;
  selectItems: () => void
}

function EnhancedTableToolbar(props: EnhancedTableToolbarProps) {
  const {numSelected, selectItems} = props;

  return (
    <Toolbar
      sx={{
        pl: {sm: 2},
        pr: {xs: 1, sm: 1},
        ...(numSelected > 0 && {
          bgcolor: (theme) =>
            alpha(theme.palette.primary.main, theme.palette.action.activatedOpacity),
        }),
      }}
    >
      {numSelected > 0 ? (
        <Typography
          sx={{flex: '1 1 100%'}}
          color="inherit"
          variant="subtitle1"
          component="div"
        >
          {numSelected} selected
        </Typography>
      ) : (
        <Typography
          sx={{flex: '1 1 100%'}}
          variant="h6"
          id="tableTitle"
          component="div"
        >
          Choose companies to explore
        </Typography>
      )}
      {numSelected > 0 ? (
        <Tooltip title="Research">
          <Button
            variant="contained"
            onClick={() => {
              selectItems()
            }}
            size={"small"}
            sx={{margin: "4px", padding: "1px", marginTop: "12px"}}
          >Research Companies</Button>
        </Tooltip>
      ) : (
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon/>
          </IconButton>
        </Tooltip>
      )}
    </Toolbar>
  );
}

function EnhancedTableRow({row, labelId, selected, setSelected}: {row: Company, labelId: string, selected: boolean, setSelected: (selected: boolean) => void}) {
  return (
    <TableRow
      hover
      onClick={() => {
        setSelected(!selected)
      }}
      role="checkbox"
      aria-checked={selected}
      tabIndex={-1}
      key={row.name}
      selected={selected}
      sx={{cursor: 'pointer'}}
    >
      <TableCell padding="checkbox">
        <Checkbox
          color="primary"
          checked={selected}
          inputProps={{
            'aria-labelledby': labelId,
          }}
        />
      </TableCell>
      <TableCell
        component="th"
        id={labelId}
        scope="row"
        padding="none"
      >
        {row.name}
      </TableCell>
      <TableCell align="right">{row.category}</TableCell>
    </TableRow>

  )
}

export default function EnhancedTable({companies, selectItems}: { companies: Company[], selectItems: (items: readonly string[]) => void }) {
  const [order, setOrder] = React.useState<Order>('asc');
  const [orderBy, setOrderBy] = React.useState<keyof Company>('name');
  const [numSelected, setNumSelected] = React.useState(companies.filter((company) => company.should_research).length)

  const handleRequestSort = (
    _event: React.MouseEvent<unknown>,
    property: keyof Company,
  ) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
    companies.sort((a, b) => (isAsc ? 1 : -1) * (a[property] as any).localeCompare(b[property]))
  };

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    for (let i = 0; i < companies.length; i++) {
      companies[i]!.should_research = event.target.checked
    }
    if (event.target.checked) {
      setNumSelected(companies.length)
    } else {
      setNumSelected(0)
    }
  };

  const setSelected = (index: number, selected: boolean) => {
    companies[index]!.should_research = selected
    setNumSelected(selected ? numSelected + 1 : numSelected - 1)
  }

  return (
      <Paper sx={{width: '100%', height: '100%', mb: 2, overflow: "hidden"}}>
        <EnhancedTableToolbar numSelected={numSelected} selectItems={() => selectItems(companies
          .filter((company) => company.should_research)
          .map((company) => company.name))}/>
        <TableContainer sx={{height: "calc(100% - 64px)"}}>
          <Table
            stickyHeader
            sx={{minWidth: 750}}
            aria-labelledby="tableTitle"
            size={'medium'}
          >
            <EnhancedTableHead
              numSelected={numSelected}
              order={order}
              orderBy={orderBy}
              onSelectAllClick={handleSelectAllClick}
              onRequestSort={handleRequestSort}
              rowCount={companies.length}
            />
            <TableBody>
              {companies.map((row, index) => {
                const labelId = `enhanced-table-checkbox-${index}`

                return (
                  <EnhancedTableRow key={row.name} row={row} labelId={labelId}
                                    selected={row.should_research}
                                    setSelected={(selected) => {
                                      setSelected(index, selected)
                                    }}
                  />
                )
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
  );
}