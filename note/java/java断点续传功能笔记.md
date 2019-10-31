### java断点续传功能
主要思路是获取上次上传的位置，从此位置开始对大文件进行分片，然后按顺序逐片上传，直至上传完成。
[参考文章](https://www.zhangxinxu.com/wordpress/2013/11/xmlhttprequest-ajax-localstorage-文件断点续传/)

还可以优化成多分片同时上传，上传完后服务器再将不同分片按顺序合并起来，加快上传速度

#### 1、模拟前端计算文件md5,对文件进行分片，并分片上传
```java
package com.cvsher.services.impl;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.RandomAccessFile;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import com.cvsher.DemoWebMain;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = { DemoWebMain.class })
public class UploadServiceTest {

	@Autowired
	UploadService service;

	@Test
	public void testSaveZip() throws Exception {
		String bigFileName = "D:\\测试文件\\3.zip";
		File originalFile = new File(bigFileName);
		RandomAccessFile raf = new RandomAccessFile(originalFile, "r");
		// 1、计算文件md5
		byte[] bytes = new byte[Integer.parseInt(raf.length() + "")];
		raf.read(bytes);
		MessageDigest md5 = MessageDigest.getInstance("MD5");
		md5.update(bytes);
		byte[] md5Bytes = md5.digest(); // 计算md5摘要
		// md5编码成base64编码输出
		Base64.Encoder encoder = Base64.getEncoder();
		String filemd5 = encoder.encodeToString(md5Bytes);
		filemd5 = filemd5.replaceAll("/", "_"); // 将斜杠转义掉，要不创建文件有问题
		System.out.println(filemd5);
		// 2、获取当前上传到哪个位置
		long startPos = service.getcurrPosByMd5(filemd5);
		// 3、文件分片，并逐片上传
		List<File> files = splitFile(startPos, raf);
		for (File f : files) {
			service.saveZip(filemd5, raf.length(), new FileInputStream(f), "3.zip"); // 逐片上传文件
		}
	}

	private List<File> splitFile(long startPos, RandomAccessFile raf) {
		List<File> files = new ArrayList<File>();
		try {
			raf.seek(startPos);
			long originalSize = raf.length();
			int perSize = 1024 * 1024 * 10; // 每片大少10兆
			byte tmpBytes[] = new byte[perSize];
			long currPos = 0;
			while (currPos < originalSize) {
				int len = raf.read(tmpBytes);
				if (len > 0) {
					currPos += len;
					File file = new File("D:\\测试文件\\3_" + currPos + ".zip");
					FileOutputStream fileOut = new FileOutputStream(file);
					fileOut.write(tmpBytes, 0, len);
					fileOut.flush();
					fileOut.close();
					files.add(file);
				} else {
					break;
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return files;
	}

}
```
#### 2、后端保存功能
```java
package com.cvsher.services.impl;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * 素材图片处理service
 * @author cvsher
 *
 */
@Service
public class UploadService {
	
	private static final Logger logger = LoggerFactory.getLogger(UploadService.class);

	private String uploadFileTmpDir;		//上传文件临时路径
	
	/**
	 * 保存zip文件包，带断点续传功能
	 * @param filemd5 整个上传文件内容的md5值
	 * @param fileSize 文件中大小
	 * @param fileIn 此次上传分片的输入流
	 * @param originalFileName 文件原名
	 * @return 整个文件所有分片上传完成返回true，否则返回false
	 */
	public boolean saveZip(String filemd5, long fileSize, InputStream fileIn, String originalFileName){
		
		long currlength = 0;		//记录此次分片上传完成后，临时文件总大小
		try(RandomAccessFile tmpFile = new RandomAccessFile(uploadFileTmpDir+filemd5+".tmp", "rw")){
			tmpFile.seek(tmpFile.length());
			byte[] tmpBytes = new byte[1024];
			int len = -1;
			while((len = fileIn.read(tmpBytes)) > 0){
				tmpFile.write(tmpBytes, 0, len);
			}
			currlength = tmpFile.length();
		}catch(Exception e){
			logger.error("保存zip文件异常", e);
		}
		//若整个文件上传完成，则重命名文件
		if(currlength >= fileSize){
			File tmp = new File(uploadFileTmpDir+filemd5+".tmp");
			File dest = new File(uploadFileTmpDir+originalFileName);
			return tmp.renameTo(dest);
		}
		return false;
	}
	
	public long getcurrPosByMd5(String filemd5){
		try (RandomAccessFile tmpFile = new RandomAccessFile("D://upload_test//"+filemd5+".tmp", "rw")){
			return tmpFile.length();
		}catch (Exception e) {
			logger.error("根据md5:"+filemd5+"获取文件已上传大小异常", e);
		}
		return 0;
	}
	
}

```