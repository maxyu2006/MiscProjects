
public class CmscTestWriter {
	public static void main(String[] args)
	{
		int numPublicTests = 20;
		int numSecretTests = 14;
		
		for(int i=1; i <= numPublicTests; i++)
		{
			if(i < 10)
				System.out.println("public0" + i + ".x | diff -u - public0" + i + ".output");
			else
				System.out.println("public" + i + ".x | diff -u - public" + i + ".output");
		}
		
		for(int i=1; i <= numSecretTests; i++)
		{
			if(i < 10)
				System.out.println("secret0" + i + ".x | diff -u - secret0" + i + ".output");
			else
				System.out.println("secret" + i + ".x | diff -u - secret" + i + ".output");
		}
	}
}
