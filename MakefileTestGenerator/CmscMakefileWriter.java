
public class CmscMakefileWriter {
	
	public static void main(String args[])
	{
		int numPublicTests = 20;
		int numSecretTests = 14;
		
		String[] constantDependencies = { "fs-sim", "driver"};
		
		String allTarget = "all: ";
		for(int i=1; i <= numPublicTests; i++)
		{
			if(i < 10)
				if(i%7 != 0)
					allTarget += "public0" + i + ".x ";
				else
					allTarget += "public0" + i + ".x \\\n\t";
			else
				if(i%7 != 0)
					allTarget += "public" + i + ".x ";
				else
					allTarget += "public" + i + ".x \\\n\t";
		}
		
		allTarget += "\\\n\t";
		for(int i=1; i <= numSecretTests; i++)
		{
			if(i < 10)
				if(i%7 != 0)
					allTarget += "secret0" + i + ".x ";
				else
					allTarget += "secret0" + i + ".x \\\n\t";
			else
				if(i%7 != 0)
					allTarget += "secret" + i + ".x ";
				else
					allTarget += "secret" + i + ".x \\\n\t";
		}
		
		System.out.println(allTarget + "\n");
		
		
		
		String xFiles = "";
		for(int i=1; i <= numPublicTests; i++)
		{
			String name = "";
			if(i < 10)
				name = "public0" + i;
			else
				name = "public" + i;
			
			xFiles += name + ".x: ";
			
			String dependencies = name + ".o";
			for(int j=0; j < constantDependencies.length; j++)
				dependencies += " " + constantDependencies[j] +".o";
			
			xFiles += dependencies + "\n\t\t$(CC) " + dependencies + " -o " + name + ".x\n\n";			
		}
		
		for(int i=1; i <= numSecretTests; i++)
		{
			String name = "";
			if(i < 10)
				name = "secret0" + i;
			else
				name = "secret" + i;
			
			xFiles += name + ".x: ";
			
			String dependencies = name + ".o";
			for(int j=0; j < constantDependencies.length; j++)
				dependencies += " " + constantDependencies[j] +".o";
			
			xFiles += dependencies + "\n\t\t$(CC) " + dependencies + " -o " + name + ".x\n\n";
		}
		System.out.println(xFiles + "\n");
		
		String oFiles = "";
		for(int i=1; i <= numPublicTests; i++)
		{
			String name = "";
			if(i < 10)
				name = "public0" + i;
			else
				name = "public" + i;
			
			oFiles += name + ".o: ";
			
			String dependencies = name + ".c";
			for(int j=0; j < constantDependencies.length; j++)
				dependencies += " " + constantDependencies[j] +".h";
			
			oFiles += dependencies + "\n\t\t$(CC) $(CCFLAGS) -c " + name + ".c\n\n";			
		}
		
		for(int i=1; i <= numSecretTests; i++)
		{
			String name = "";
			if(i < 10)
				name = "secret0" + i;
			else
				name = "secret" + i;
			
			oFiles += name + ".o: ";
			
			String dependencies = name + ".c";
			for(int j=0; j < constantDependencies.length; j++)
				dependencies += " " + constantDependencies[j] +".h";
			
			oFiles += dependencies + "\n\t\t$(CC) $(CCFLAGS) -c " + name + ".c\n\n";			
		}
		System.out.println(oFiles);
	}

}
