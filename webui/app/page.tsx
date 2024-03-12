import { redirect } from "next/navigation";
import { getServerSession } from "next-auth";

export const runtime = 'nodejs';

export default async function IndexPage() {
  const session = await getServerSession();

  if (!session?.user) {
    redirect(`/sign-in?next=/`);
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Welcome to the Crime Analysis Tool</h1>
      
      <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-6" role="alert">
        <p className="font-bold">Important:</p>
        <p>Click on site settings for this website and allow insecure content. Our backend runs HTTP and needs this to communicate with the frontend.</p>
      </div>
      
      <div style={{ maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}>
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">Getting Started</h2>
          <ol className="list-decimal list-inside">
            <li>Click on "New Chat" to create a new chat session.</li>
            <li>Choose a name for your chat.</li>
            <li>
              Select the appropriate agent:
              <ul className="list-disc list-inside ml-6">
                <li>Choose "Crime Agent" if you want to make your query in natural language.</li>
                <li>Choose "SQL" if you want to make your query in SQL.</li>
              </ul>
            </li>
          </ol>
        </div>
        
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">Data Schema</h2>
          <p className="mb-2">All fields are treated as strings:</p>
          <ul className="list-disc list-inside">
            <li>IncidentDatetime</li>
            <li>IncidentDate</li>
            <li>IncidentTime</li>
            <li>IncidentYear</li>
            <li>IncidentDayOfWeek</li>
            <li>ReportDatetime</li>
            <li>RowID</li>
            <li>IncidentID</li>
            <li>IncidentNumber</li>
            <li>CADNumber</li>
            <li>ReportTypeCode</li>
            <li>ReportTypeDescription</li>
            <li>FiledOnline</li>
            <li>IncidentCode</li>
            <li>IncidentCategory</li>
            <li>IncidentSubcategory</li>
            <li>IncidentDescription</li>
            <li>Resolution</li>
            <li>Intersection</li>
            <li>CNN</li>
            <li>PoliceDistrict</li>
            <li>AnalysisNeighborhood</li>
            <li>SupervisorDistrict</li>
            <li>SupervisorDistrict2012</li>
            <li>Latitude</li>
            <li>Longitude</li>
            <li>Point</li>
            <li>Neighborhoods</li>
            <li>ESNCAGBoundaryFile</li>
            <li>CentralMarketTenderloinBoundaryPolygonUpdated</li>
            <li>CivicCenterHarmReductionProjectBoundary</li>
            <li>HSOCZonesAsOf20180605</li>
            <li>InvestInNeighborhoodsAreas</li>
            <li>CurrentSupervisorDistricts</li>
            <li>CurrentPoliceDistricts</li>
          </ul>
        </div>
        
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">Incident Categories</h2>
          <ul className="list-disc list-inside">
            <li>Motor Vehicle Theft</li>
            <li>Case Closure</li>
            <li>Stolen Property</li>
            <li>Disorderly Conduct</li>
            <li>Drug Offense</li>
            <li>Drug Violation</li>
            <li>Weapons Offense</li>
            <li>Vandalism</li>
            <li>Robbery</li>
            <li>Vehicle Impounded</li>
            <li>Suicide</li>
            <li>Civil Sidewalks</li>
            <li>Courtesy Report</li>
            <li>Fire Report</li>
            <li>NULL</li>
            <li>Rape</li>
            <li>Assault</li>
            <li>Gambling</li>
            <li>Human Trafficking (A)</li>
            <li>Non-Criminal</li>
            <li>Lost Property</li>
            <li>Traffic Collision</li>
            <li>Forgery And Counterfeiting</li>
            <li>Sex Offense</li>
            <li>Homicide</li>
            <li>Liquor Laws</li>
            <li>Weapons Offence</li>
            <li>Malicious Mischief</li>
            <li>Weapons Carrying Etc</li>
            <li>Other Offenses</li>
            <li>Motor Vehicle Theft?</li>
            <li>Suspicious</li>
            <li>Burglary</li>
            <li>Missing Person</li>
            <li>Fraud</li>
            <li>Human Trafficking (B)</li>
            <li>Other Miscellaneous</li>
            <li>Miscellaneous Investigation</li>
            <li>Suspicious Occ</li>
            <li>Other</li>
            <li>Traffic Violation Arrest</li>
            <li>Human Trafficking</li>
            <li>Larceny Theft</li>
            <li>Recovered Vehicle</li>
            <li>Arson</li>
            <li>Embezzlement</li>
            <li>Warrant</li>
            <li>Offences Against The Family And Children</li>
            <li>Prostitution</li>
            <li>Vehicle Misplaced</li>
          </ul>
        </div>
        
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-2">Date Range</h2>
          <p>The last crime recorded in this database happened on February 16th, 2023.</p>
          <p>The earliest crime in this database happened on January 1st, 2018.</p>
        </div>
      </div>
    </div>
  );
}
