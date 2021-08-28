import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;

public class JapaneseDrillMaker {
	
	public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException
	{
		
		PrintWriter writer = new PrintWriter("Drills.txt", "UTF-8");
		
		File file = new File("C:/Users/maxyu/Documents/Japanese/JSL/content/Sound/");
		File ankiDir = new File("C:/Users/maxyu/Documents/Anki/User 1/collection.media/");
		
		File[] subDirectories = file.listFiles();
		
		//go through each lesson folder
		for(int i=0; i < subDirectories.length; i++)
			if(subDirectories[i].isDirectory())
			{
				//checks if 
				File[] tempSub = subDirectories[i].listFiles();
				
				//search for the drill folder in each lesson folders
				for(int j=0; j < tempSub.length; j++)
					if(tempSub[j].getName().equals("Drills"))
					{
						File[] tempSubDrills = tempSub[j].listFiles();
						
						String seriesCue = "";
						String seriesResp = "";
						
						//go through the each mp3 file in the drill folder
						for(int k = 0; k < tempSubDrills.length; k++)
						{	
							if(tempSubDrills[k].isFile())
							{
								//copy the file into the anki folder
								//Files.copy(tempSubDrills[k].ge, ankiDir.getPath());
								//System.out.println(tempSubDrills[k].getPath());
								//System.out.println(ankiDir.getPath());
								
								String name = tempSubDrills[k].getName();
								String[] splitName = name.split("-");
								
								System.out.println(name);
								
								String label = splitName[0];
								String number;
								String series;
								
								if(splitName[0].equals("D30A") && splitName[1].charAt(0) == 'K')
									System.out.println("reached the problem");
								
								//search for the series with modified series
								//store the series (the drill number A,B,C etc) and 
								//the drill subnumber (1, 2 3, etc)
								if(splitName[1].contains("'"))
								{
									series = splitName[1].substring(0, 2);
									number = splitName[1].substring(2, splitName[1].length()-7);
								}
								else
								{
									series = splitName[1].substring(0, 1);
									number = splitName[1].substring(1, splitName[1].length()-7);
								}//endif
								
								
								if((number.charAt(0) == '1' && number.length() == 1) ||
										(number.charAt(0) == '1' && number.charAt(1) == 'r'))
								{
									if(splitName[1].contains("cue"))
										seriesCue = "[sound:" + name + "]";
									else if(splitName[1].contains("resp"))
										seriesResp = "[sound:" + name + "]";
									
									//System.out.println(seriesCue + seriesResp);
								}
								else
								{									
									//check to make sure there is a seriesCue and SeriesResp
									//that was detected
									if(seriesCue.isEmpty() || seriesResp.isEmpty())
										System.out.println("Error reading series");
									
									if(name.contains("cue"))
									{
										//build filenames for cue and response tracks
										String cue = label +"-" +series +number+"cue.mp3";
										String resp = label+"-" +series +number+"resp.mp3";
										
										//make filenames sound tracks for anki
										cue = "[sound:" + cue + "]";
										resp = "[sound:" + resp + "]";
										
										//build csv line
										String csvString = label+series + number + "," + seriesCue + "," + seriesResp;
										csvString += "," + cue + "," + resp + "," + label;
										
										//System.out.println(csvString);
										
										writer.println(csvString);
									}//endif
								}//endif
							}//end if
						}//end for
					}//endif
			}//end if
		
		writer.close();
	}//END MAIN

}//end class
